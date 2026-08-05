---
name: codelevels-environment
description: Run Python and Django commands in the Poetry-managed virtual environment for CodeLevels.net (code-levels-railway). Use when running terminal commands, migrations, manage.py, tests, scripts, or installing dependencies in this repository.
---

# CodeLevels Environment

Django project **CodeLevels.net** (`code-levels-railway`). Dependencies and the virtual environment are managed by **Poetry** (`pyproject.toml`, `poetry.lock`).

There is **no committed in-repo venv** — `.venv/` and `venv/` are gitignored. On this machine Poetry stores the environment in its global cache.

## Virtualenv location (current)

| | Path |
|---|------|
| **Venv root** | `C:/Users/adm/AppData/Local/pypoetry/Cache/virtualenvs/code-levels-railway-_1ITifYl-py3.14` |
| **Python** | `.../Scripts/python.exe` |
| **Activate (Git Bash)** | `source C:/Users/adm/AppData/Local/pypoetry/Cache/virtualenvs/code-levels-railway-_1ITifYl-py3.14/Scripts/activate` |

Poetry may recreate the env after Python upgrades or `poetry env remove`. **Always resolve the live path with:**

```bash
poetry env info -p
```

Do **not** hard-code a stale path in new scripts — use `poetry run` or query `poetry env info -p` first.

## Running commands (preferred)

Use `poetry run` from the repo root so commands use the project venv without manual activation:

```bash
cd d:/Coding/django/code-levels-railway

poetry run python manage.py migrate
poetry run python manage.py runserver
poetry run python manage.py makemigrations platform_web
poetry run python manage.py shell
poetry run pytest
```

Interactive shell inside the venv:

```bash
poetry shell
```

## Django settings & env files

- `manage.py` loads `.env` via `python-dotenv`
- Default settings module: `code_levels.settings.dev` (see `code_levels/settings/config/Dotenv.py`)
- Local env files (gitignored): `.env`, `.env.dev`, `.env.prod`

If `python manage.py` fails with `ModuleNotFoundError: dotenv`, the system Python was used — switch to `poetry run`.

## Dependencies

```bash
poetry install              # install/sync from lock file
poetry add <package>        # add runtime dependency
poetry add --group dev <package>   # dev dependency (if group used)
```

Legacy `requirements.txt` exists but **Poetry is the source of truth** for local development.

## Python version

- Declared in `pyproject.toml`: `>=3.13,<4`
- Current venv: **Python 3.14.2** (CPython, Windows)

## Common mistakes

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No module named 'dotenv'` | Ran bare `python manage.py` | Use `poetry run python manage.py ...` |
| Wrong Django / missing packages | Wrong interpreter | `poetry env info` → confirm path |
| Stale activate path | Poetry recreated venv | `poetry env info -p` → update activation |

## Related skills

- **Project conventions:** `.agents/skills/development/code-style/SKILL.md`
- **Refactor / cleanup:** `.agents/skills/development/refactor/SKILL.md`
- **Known pitfalls:** `.agents/skills/development/mistakes/MISTAKES.md`
