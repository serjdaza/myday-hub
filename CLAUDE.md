# CLAUDE.md

myday-hub: a personal calendar aggregator (Google Calendar + Outlook). It will be deployed to a k3s homelab.
The owner is learning, so keep changes small and explain the reasoning behind them.

## Layout
- `backend/app/`: FastAPI app. `config.py` (env settings), `db.py` (engine/session/Base), `models.py` (ORM), `schemas.py` (Pydantic API shapes), `api/` (one router module per area)
- `backend/alembic/versions/`: database migrations
- `backend/tests/`: pytest
- `frontend/`: React + TS + Vite. In dev, `/api` is proxied to the backend
- `Dockerfile`: multi-stage build. The `dev` target is used by compose, and `prod` (the default) is one image that serves the API plus the built frontend
- `docker-compose.yml`: local dev only (db, api, web)

## Conventions
- **Config comes only from env vars.** Add a new setting to `app/config.py` AND `.env.example`. Never commit `.env` or secrets.
- **Schema changes need an Alembic migration.** Autogenerate it, then review it. Never edit a migration that has already been applied; add a new one instead.
- **Endpoints** go in `app/api/<area>.py`, are mounted under `/api`, and return Pydantic schemas (`response_model`), not raw ORM objects.
- Use the sync SQLAlchemy 2.x style: `Mapped[...]`, `mapped_column`, `select()`. Get a session from the `get_db` dependency.
- Every new endpoint gets a pytest test. Tests override `get_db` when they don't need a real DB.
- Frontend code calls relative URLs (`/api/...`) and never hard-codes hosts.
- Don't add calendar integrations or other new features unless asked.

## Commands
- Dev: `cp .env.example .env && docker compose up --build`
- Tests: `docker compose run --rm api pytest`
- New migration: `docker compose run --rm api alembic revision --autogenerate -m "..."`
- Prod image: `docker build -t myday-hub .`
