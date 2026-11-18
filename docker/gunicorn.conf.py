# Gunicorn configuration for Horilla-HR
# This file provides advanced configuration options for the WSGI server

import multiprocessing
import os

from gunicorn.glogging import Logger, SafeAtoms

# Bind settings
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"
host = "0.0.0.0"
port = int(os.environ.get("PORT", "8000"))

# Worker settings
# `or`, not a get() default: docker-compose.prod.yml passes GUNICORN_WORKERS
# through as an empty string when .env leaves it unset, and int("") crashes.
workers = int(
    os.environ.get("GUNICORN_WORKERS")
    or max(2, min(multiprocessing.cpu_count() * 2 + 1, 8))
)
worker_class = "gthread"
threads = 4
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
# preload_app is disabled with gthread workers to avoid ORM connection issues
preload_app = False

# Timeout settings
timeout = 120
keepalive = 5

# Logging
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("GUNICORN_LOG_LEVEL", "info")


_RAW_JSON_ATOMS = ("req_body", "resp_body")


class _BodyAtoms(SafeAtoms):
    """SafeAtoms, minus quote-escaping for the JSON body atoms.

    SafeAtoms turns every ``"`` into ``\\"``, which makes JSON unreadable.
    The body atoms are json.dumps output (no raw newlines or control chars),
    so leaving their quotes alone cannot forge a log line.
    """

    def __init__(self, atoms):
        super().__init__(atoms)
        for key in _RAW_JSON_ATOMS:
            if key in atoms:
                dict.__setitem__(self, key, atoms[key])


class HorillaAccessLogger(Logger):
    """Adds a ``%(ms)s`` atom: request time in milliseconds, 2 decimals.

    Gunicorn's built-in ``%(M)s`` is an integer and ``%(D)s`` is microseconds.
    """

    atoms_wrapper_class = _BodyAtoms

    def atoms(self, resp, req, environ, request_time):
        atoms = super().atoms(resp, req, environ, request_time)
        atoms["ms"] = "%.2fms" % (request_time.total_seconds() * 1000)
        # Set by horilla.observability.AccessLogBodyMiddleware: already
        # scrubbed, JSON-only and clipped to 256 chars. Literal key strings
        # rather than importing Django code into the gunicorn master.
        atoms["req_body"] = environ.get("horilla.access_log.req_body", "-")
        atoms["resp_body"] = environ.get("horilla.access_log.resp_body", "-")
        return atoms


logger_class = HorillaAccessLogger

# %({x-request-id}o)s is the X-Request-ID response header set by
# horilla.observability.RequestIDMiddleware, so an access line can be joined
# to the app's JSON log lines. Shows "-" for responses that never reached the
# middleware (e.g. static files served earlier in the stack).
access_log_format = (
    '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" '
    "req_id=%({x-request-id}o)s %(ms)s "
    "req_body=%(req_body)s resp_body=%(resp_body)s"
)

# Process naming
proc_name = "horilla-hrms"

# Server mechanics
pidfile = "/tmp/gunicorn.pid"
user = None  # Run as current user in container
group = None
tmp_upload_dir = None

# Development settings
reload = os.environ.get("GUNICORN_RELOAD", "false").lower() == "true"

# SSL settings (if needed)
# ssl_keyfile = os.environ.get('SSL_KEYFILE')
# ssl_certfile = os.environ.get('SSL_CERTFILE')
