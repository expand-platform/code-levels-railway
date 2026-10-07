---
name: codelevels-environment
description: >-
  Run Python and Django commands in the Poetry-managed virtualenv for
  CodeLevels.net. Use when running manage.py, scripts, migrations, or
  installing dependencies. Do not write or run tests unless the user
  explicitly asks in the current request.
---

# CodeLevels Environment

Poetry owns the venv (`pyproject.toml`, `poetry.lock`). No in-repo `.venv/`.
Resolve the live path with `poetry env info -p` — do not hard-code it.

Do not add tests, edit `platform_web/tests.py`, or run `pytest` / the test suite unless the user explicitly asks in the current request. `poetry run pytest` below is only for that case.

```bash
cd d:/Coding/django/code-levels-railway
poetry run python manage.py runserver
poetry run python manage.py makemigrations platform_web
poetry run python manage.py sqlmigrate platform_web <number>
poetry run python manage.py migrate --plan
poetry run python manage.py shell
poetry run python manage.py check
poetry run pytest
poetry install
poetry add <package>                 # runtime
poetry add --group dev <package>     # dev
```

**Migrations:** generate with `makemigrations`, then check with `sqlmigrate` and `migrate --plan`. Do **not** apply them (`migrate`) unless the user explicitly asks.

- `manage.py` loads `.env` via `python-dotenv`; default settings: `code_levels.settings.dev`
- Local env files (gitignored): `.env`, `.env.dev`, `.env.prod`
- Python: `>=3.13,<4` in `pyproject.toml`. `requirements.txt` is legacy — Poetry is source of truth.
- Makefile targets still call bare `python` — agents should use `poetry run` anyway.

| Symptom | Fix |
|---------|-----|
| `No module named 'dotenv'` | Bare `python` — use `poetry run python manage.py ...` |
| Wrong Django / missing packages | `poetry env info`, then that interpreter |
| Stale activate path | `poetry env info -p` after Poetry recreates the env |
