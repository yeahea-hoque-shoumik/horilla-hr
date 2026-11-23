# Security and access

## Summary

This area covers how people sign in and how the system protects itself: passwords and lockout, optional two-step sign-in, session time-outs, sign-in tokens for the mobile app, limits on how often requests can be made, and checks before the system starts in production. It also records two risks introduced by this fork: protections lost when the web server gatekeeper was removed, and an access log that can record pay amounts and personal details.

## Who uses it

- Every user signs in.
- Administrators and the people running the servers set the security settings.

## Features

### Signing in

- Users sign in with a user name and password.
- Rule: after 5 failed attempts, sign-in is locked for 30 minutes for that user name from that network address. Reason: not stated in the code.
- An optional second step sends a one-time code by e-mail; it is off by default.
- Users must change their password the first time they sign in, and can reset a forgotten password by e-mail.

### Sessions

- Rule: a session ends after 12 hours without activity, and every request renews it. Reason: not stated in the code.

### Mobile app sign-in

- The mobile app gets an access token that lasts 60 minutes and a refresh token that lasts 30 days. Each refresh gives a new refresh token and cancels the old one; signing out cancels the token; changing the password cancels existing tokens.
- Rule: requests are limited per minute: 60 for visitors who are not signed in, 600 for signed-in users, 12 sign-in attempts, and 6 bulk actions. Reason: not stated in the code.

### Production start-up check and other protections

- The system refuses to start in production with a default secret key, with no limit on the host names it answers to, or with the default setup password (see [Organisation and company setup](01-organisation-and-company-setup.md)).
- In production, sign-in cookies are sent only over secure connections.
- Every save checks text for **cross-site scripting**; uploaded SVG images are checked; payroll tax formulas run in a restricted, time-limited sandbox (see [Payroll](07-payroll.md)).

### Protections removed by this fork

> Flag (risk): this fork removed the nginx web server gatekeeper from production (commit fb8ff8eec, 2026-11-16). The limits that nginx applied no longer protect the system: at most 5 sign-in attempts per minute, a block on the technical metrics page, and a 50 MB limit on uploads (`docker/nginx.conf`, `docker-compose.prod.yml`). The metrics page is still limited to staff users in the code. Business effect: password-guessing is slowed only by the 30-minute lockout and the 12-per-minute mobile app limit, and very large uploads can reach the application and slow it down or fill its disk. The address used for lockout and for the office network check also depends on a correct setting; see [Attendance](05-attendance.md).

### The fork's new access log

> Flag (risk): the access log added by this fork records shortened copies of request and response contents. Fields that look like salary are blanked out, but net pay, gross pay, wage, names and e-mail addresses are not (`horilla/observability.py`). Business effect: people who can read the server logs can see employees' pay and personal details, which may break privacy rules and company policy.

## Who can do what

| Action | Who |
|---|---|
| Sign in | Every user with an active account that is not blocked |
| Block or unblock an account | People with the account block permission (Admin) |
| Change security settings (lockout, two-step sign-in, tokens, limits) | The people running the servers, through server settings; not through screens |
| See the technical metrics page | Staff users only |

These come from the settings and the permission checks on the account screens (`horilla/settings/base.py`, `base/views.py`).

## Recommendations

- Suggestion: put a gatekeeper back in front of the system (or add the same limits inside the application): a stricter sign-in rate limit, an upload size limit, and a block on the metrics page.
- Suggestion: blank out pay amounts, names and e-mail addresses in the access log, or stop recording response contents.
- Suggestion: consider switching on the two-step sign-in for HR, payroll and admin roles.

## Related documents

- [How the system works overall](00-how-the-system-works.md): the fork's changes.
- [Mobile app API](22-mobile-app-api.md): what the mobile app tokens give access to.

## Change log

| Date | What changed | Who changed it |
|---|---|---|
| 2026-11-19 | First version. | Claude (AI-DLC developer agent) |
