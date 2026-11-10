---
name: verify
description: Smoke-test the Django portfolio after changes (system check, pending migrations, key pages return 200). Use after editing models, views, templates, URLs or settings, since the repo has no test suite.
---

The repo has no tests, so verify changes against the running Docker stack.

1. Make sure the stack is up: `docker compose ps`. If `portfolio_web` isn't running, start it with `docker compose -f docker-compose.yml -f docker-compose.dev.yml up --build -d`. Never use the production-only file locally, because it requires TLS certificates. Otherwise run `docker compose restart web` so code changes are picked up, because gunicorn doesn't reload.
2. `docker exec portfolio_web python manage.py check`
3. `docker exec portfolio_web python manage.py makemigrations --check --dry-run`. If it fails, models changed without a migration. Create one with `docker exec portfolio_web python manage.py makemigrations`, then run `migrate`.
4. Check the pages through nginx. Each should return 200:
   ```bash
   for p in / /projects/ /contact/; do echo "$p $(curl -s -o /dev/null -w '%{http_code}' http://localhost$p)"; done
   ```
   For a project detail page, also check `/projects/<slug>/` using a slug that exists. For HTMX partials, send the header `-H 'HX-Request: true'`.
5. If anything fails, show the error with `docker compose logs --tail=50 web`.

Report a pass or fail for each step. Don't push afterwards: pushing to `main` deploys to production.
