# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Dev workflow (Docker-first)

- Run locally with `docker compose up --build` (services `web` = gunicorn, `nginx` on :80). Run all Django commands inside the container: `docker exec portfolio_web python manage.py <cmd>`.
- gunicorn has no `--reload`: after Python/template changes run `docker compose restart web`.
- The repo is bind-mounted into `/app`, so `db.sqlite3` on the host is the live DB.
- No tests exist. Verify changes with `/verify`.
- Lint/format: `ruff check .` / `ruff format .` (config in `ruff.toml`, ruff installed on the host, not in the container). A hook auto-formats edited `.py` files.

## Git & deploy

- **Every push to `main` deploys to production** (vhmedeiros.dev.br via `.github/workflows/deploy.yml`: git pull, compose build, migrate, collectstatic on the VM). Commit locally, but **never push**; the user pushes.
- Commit messages: Conventional Commits (`feat:`, `fix:`, `ci:`…) with the description in Portuguese, e.g. `feat: adiciona filtro por tag`.
- Never commit secrets (`.env`, keys, passwords). Config comes from env vars read in `config/settings.py`: `SECRET_KEY`, `DEBUG` (only the exact string `"True"` enables it), `ALLOWED_HOSTS` (comma-separated), `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` (Gmail SMTP; also used as the contact recipient).

## Conventions

- UI text is Portuguese (pt-br).
- Frontend: server-rendered templates + HTMX (CDN) + Tailwind v3. No Node/npm — don't add one.
- Tailwind is compiled by the standalone CLI (`~/.local/bin/tailwindcss`) from `assets/tailwind.css` + `tailwind.config.js` into `core/static/core/css/site.css`, which **is committed** (the compose bind mount `.:/app` means the host file is what gets served; deploy is just `git pull`). A hook rebuilds it after template edits; rebuild manually with `tailwindcss -i assets/tailwind.css -o core/static/core/css/site.css --minify` (add `--watch` while editing by hand). Never edit `site.css` directly.
- Custom CSS goes in `assets/tailwind.css` under `@layer components` (so utilities still win); classes added only at runtime by JS/HTMX (e.g. `.htmx-request`) must stay outside any `@layer` or Tailwind purges them.
- HTMX views return a partial from `<app>/templates/<app>/partials/` when `request.htmx` is set; keep full page and partial in sync.
- Static files use whitenoise `CompressedManifestStaticFilesStorage`: always reference them with `{% static %}`; a missing file errors when DEBUG is off.
- Project content (projects, tags, images) is managed via Django admin; `full_description` is Markdown rendered by `render_markdown` (`projects/templatetags/markdown_tags.py`) without sanitization — admin-only trusted input.
