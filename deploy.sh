#!/usr/bin/env bash
# Deploy Horilla HR to production with Docker on this host.
#
# Runs the same stack as `make prod` (docker-compose.yml + docker-compose.prod.yml:
# web, scheduler), configured from .env. Gunicorn is served directly on host
# port 1000 (no nginx; Cloudflare sits in front). PostgreSQL and Redis are the ones already running on this host
# (the postgres_db and redis containers), reached at 172.17.0.1.
#
# Usage:
#   ./deploy.sh init-env <domain> [--db-user USER] [--force]
#                                             Write a production .env with random secrets.
#                                             With --db-user, the password is taken from
#                                             DB_PASSWORD or asked for (hidden).
#   ./deploy.sh setup-db                      Create Horilla's user + database in postgres_db
#   ./deploy.sh [--skip-backup]               Check .env, back up the DB, build, start, verify
#   ./deploy.sh status                        Show containers
#   ./deploy.sh logs [service]                Follow logs
#   ./deploy.sh stop                          Stop the stack (data is kept)

set -Eeuo pipefail
cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")"

ENV_FILE=".env"
BACKUP_DIR="backups"
HTTP_PORT=1000
HOST_IP=172.17.0.1    # Docker bridge gateway: the host, as seen from containers
PG_CONTAINER=postgres_db
WAIT_TIMEOUT="${WAIT_TIMEOUT:-600}" # first start runs every migration
export HTTP_PORT

COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.prod.yml --env-file "$ENV_FILE")

step() { printf '\n==> %s\n' "$*"; }
info() { printf '    %s\n' "$*"; }
die()  { printf '\nERROR: %s\n' "$*" >&2; exit 1; }

usage() { sed -n '2,/^$/{s/^# \{0,1\}//;p}' "$0"; }

# Read KEY from .env without sourcing it (secrets may contain shell characters).
env_get() {
  local line
  line="$(grep -E "^${1}=" "$ENV_FILE" 2>/dev/null | tail -n 1 || true)"
  printf '%s' "${line#*=}"
}

# Split DATABASE_URL (postgres://user:password@host:port/name) into DB_USER,
# DB_PASS and DB_NAME.
parse_db_url() {
  local url
  url="$(env_get DATABASE_URL)"
  [[ "$url" =~ ^postgres(ql)?://([^:@/]+):([^@]*)@[^/]+/([^?]+) ]] \
    || die "DATABASE_URL must look like postgres://USER:PASSWORD@${HOST_IP}:5432/NAME"
  DB_USER="${BASH_REMATCH[2]}" DB_PASS="${BASH_REMATCH[3]}" DB_NAME="${BASH_REMATCH[4]}"
}

# Letters and digits only: safe in .env, in Compose, and inside URLs.
random_string() {
  LC_ALL=C tr -dc 'A-Za-z0-9' </dev/urandom | head -c "$1" || true
}

check_env() {
  step "Checking $ENV_FILE"
  [ -f "$ENV_FILE" ] || die "$ENV_FILE not found. Create it with: ./deploy.sh init-env <your-domain>"

  local key errors=()
  for key in SECRET_KEY ALLOWED_HOSTS CSRF_TRUSTED_ORIGINS DATABASE_URL DB_INIT_PASSWORD REDIS_URL; do
    case "$(env_get "$key")" in
      "") errors+=("$key is not set") ;;
      *change-me*) errors+=("$key still has the change-me placeholder") ;;
    esac
  done
  # The container health check calls http://localhost:8000/health/; without
  # localhost here Django rejects it and the stack never becomes healthy.
  [[ "$(env_get ALLOWED_HOSTS)" != *example.com* ]] \
    || errors+=("ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS still have the placeholder hr.example.com; put your subdomain there")
  [[ ",$(env_get ALLOWED_HOSTS)," == *",localhost,"* ]] \
    || errors+=("ALLOWED_HOSTS must include localhost (e.g. hr.example.com,localhost)")

  if [ "${#errors[@]}" -gt 0 ]; then
    printf '    - %s\n' "${errors[@]}" >&2
    die "$ENV_FILE is not ready for production. Write one with: ./deploy.sh init-env <domain> --force"
  fi
  "${COMPOSE[@]}" config --quiet || die "docker compose rejected the configuration."
  info "ok"
}

# Create the role and database named in DATABASE_URL, if they don't exist yet.
# Runs psql inside postgres_db as its admin user over the local socket; the SQL
# (with the password) goes in on stdin so it never shows in the process list.
cmd_setup_db() {
  [ -f "$ENV_FILE" ] || die "$ENV_FILE not found. Run ./deploy.sh init-env <domain> first."
  parse_db_url
  [[ "$DB_USER$DB_NAME" =~ ^[A-Za-z0-9_]+$ ]] || die "Database user and name may only use letters, digits and _."
  [[ "$DB_PASS" != *"'"* ]] || die "The database password must not contain a single quote."
  local admin
  admin="$(docker inspect -f '{{range .Config.Env}}{{println .}}{{end}}' "$PG_CONTAINER" | sed -n 's/^POSTGRES_USER=//p')"
  admin="${admin:-postgres}"
  step "Creating role $DB_USER and database $DB_NAME in $PG_CONTAINER (as $admin)"
  docker exec -i "$PG_CONTAINER" psql -v ON_ERROR_STOP=1 -q -U "$admin" -d postgres <<SQL
SELECT format('CREATE ROLE %I LOGIN PASSWORD %L', '$DB_USER', '$DB_PASS')
  WHERE NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$DB_USER') \gexec
SELECT format('CREATE DATABASE %I OWNER %I', '$DB_NAME', '$DB_USER')
  WHERE NOT EXISTS (SELECT 1 FROM pg_database WHERE datname = '$DB_NAME') \gexec
SQL
  info "ok. Next: ./deploy.sh"
}

backup_db() {
  step "Backing up the database"
  parse_db_url
  local file
  file="$BACKUP_DIR/db_$(date +%Y%m%d_%H%M%S).dump"
  mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
  if ! docker exec "$PG_CONTAINER" pg_dump -U "$DB_USER" -d "$DB_NAME" -Fc >"$file" || [ ! -s "$file" ]; then
    rm -f "$file"
    die "Database backup failed; not deploying. Has ./deploy.sh setup-db been run? (--skip-backup skips this.)"
  fi
  chmod 600 "$file"
  info "Saved $file (restore: docker exec -i $PG_CONTAINER pg_restore -U $DB_USER -d $DB_NAME --clean < $file)"
}

wait_for_web() {
  step "Waiting for the app to become healthy (up to ${WAIT_TIMEOUT}s)"
  local id status="" elapsed=0
  while [ "$elapsed" -lt "$WAIT_TIMEOUT" ]; do
    id="$("${COMPOSE[@]}" ps -q web 2>/dev/null || true)"
    status="$(docker inspect -f '{{.State.Status}}/{{if .State.Health}}{{.State.Health.Status}}{{end}}' "$id" 2>/dev/null || true)"
    case "$status" in
      running/healthy) info "healthy after ${elapsed}s"; return 0 ;;
      exited/*|dead/*) break ;;
    esac
    sleep 5
    elapsed=$((elapsed + 5))
  done
  "${COMPOSE[@]}" logs --tail 60 web >&2 || true
  die "web did not become healthy (state: ${status:-unknown}). See: ./deploy.sh logs web"
}

cmd_deploy() {
  local skip_backup=0
  case "${1:-}" in
    "") ;;
    --skip-backup) skip_backup=1 ;;
    *) die "Unknown option: $1" ;;
  esac

  command -v docker >/dev/null && docker compose version >/dev/null 2>&1 \
    || die "Docker with the Compose plugin is required."
  check_env
  if [ "$skip_backup" -eq 0 ]; then backup_db; fi

  step "Building images"
  "${COMPOSE[@]}" build

  # Migrations and collectstatic run in the web container's entrypoint.
  step "Starting the stack"
  "${COMPOSE[@]}" up -d --remove-orphans

  wait_for_web

  step "Checking the app on port $HTTP_PORT"
  local code
  code="$(curl -s -o /dev/null -w '%{http_code}' --max-time 10 "http://localhost:$HTTP_PORT/health/" || echo 000)"
  [[ "$code" == [23]?? ]] || die "The app did not answer on http://localhost:$HTTP_PORT/ (HTTP $code). See: ./deploy.sh logs web"
  info "HTTP $code"

  docker image prune -f >/dev/null || true
  printf '\nDeployed. Horilla HR is running on http://localhost:%s/ (https://%s/ through your tunnel).\n' \
    "$HTTP_PORT" "$(env_get ALLOWED_HOSTS | cut -d, -f1)"
}

cmd_init_env() {
  local domain="" force=0 db_user="horilla_user"
  while [ "$#" -gt 0 ]; do
    case "$1" in
      --force) force=1 ;;
      --db-user) [ "$#" -ge 2 ] || die "--db-user needs a value"; db_user="$2"; shift ;;
      -*) die "Unknown option: $1" ;;
      *) domain="$1" ;;
    esac
    shift
  done
  [ -n "$domain" ] || die "Usage: ./deploy.sh init-env hr.example.com [--db-user USER] [--force]"

  # An existing login brings its own password; a new horilla_user gets a random one.
  local pg_pass="${DB_PASSWORD:-}"
  if [ "$db_user" != "horilla_user" ] && [ -z "$pg_pass" ]; then
    [ -t 0 ] || die "Set DB_PASSWORD for --db-user $db_user."
    read -r -s -p "Password for database user $db_user: " pg_pass; printf '\n'
  fi
  pg_pass="${pg_pass:-$(random_string 40)}"
  [[ "$pg_pass" =~ ^[A-Za-z0-9._~-]+$ ]] \
    || die "Use a database password of letters, digits and . _ ~ - only (other characters need URL-encoding)."

  if [ -e "$ENV_FILE" ]; then
    [ "$force" -eq 1 ] || die "$ENV_FILE already exists. Add --force to replace it (the old one is kept in $BACKUP_DIR/)."
    mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
    cp -p "$ENV_FILE" "$BACKUP_DIR/env_$(date +%Y%m%d_%H%M%S)"
    info "Saved the old $ENV_FILE in $BACKUP_DIR/"
  fi

  (
    umask 077
    cat >"$ENV_FILE" <<EOF
# Horilla HR production settings, written by ./deploy.sh init-env. Never commit this file.
# Full variable reference: .env.dist
DJANGO_SETTINGS_MODULE=horilla.settings
HORILLA_ENV=production
DEBUG=False

SECRET_KEY=$(random_string 64)
# Keep localhost: the container health check uses it.
ALLOWED_HOSTS=${domain},localhost
CSRF_TRUSTED_ORIGINS=https://${domain}
TIME_ZONE=Asia/Kolkata
SECURE_SSL_REDIRECT=False
AXES_PROXY_COUNT=1

# Password for the first-run database setup page.
DB_INIT_PASSWORD=$(random_string 48)

# Existing PostgreSQL (postgres_db) and Redis (redis) on this host.
# ./deploy.sh setup-db creates the horilla_db database (and the user, if new).
DATABASE_URL=postgres://${db_user}:${pg_pass}@${HOST_IP}:5432/horilla_db
DB_HOST=${HOST_IP}
DB_PORT=5432
REDIS_URL=redis://${HOST_IP}:6379/0
EOF
  )
  info "Wrote $ENV_FILE for $domain. Next: ./deploy.sh setup-db, then ./deploy.sh"
}

case "${1:-deploy}" in
  deploy) shift || true; cmd_deploy "$@" ;;
  --skip-backup) cmd_deploy "$@" ;;
  init-env) shift; cmd_init_env "$@" ;;
  setup-db) cmd_setup_db ;;
  status) "${COMPOSE[@]}" ps ;;
  logs) shift; "${COMPOSE[@]}" logs -f --tail 200 "$@" ;;
  stop) "${COMPOSE[@]}" down ;;
  -h|--help|help) usage ;;
  *) usage; die "Unknown command: $1" ;;
esac
