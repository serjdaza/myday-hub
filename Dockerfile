# One Dockerfile, several stages. Build targets:
#   docker build -t myday-hub .            -> prod (the last stage, default)
#   docker compose up                      -> uses the "dev" target

# ---- 1. Build the React app into static files ----
FROM node:22-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

# ---- 2. Python base: dependencies + backend code ----
FROM python:3.12-slim AS base
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /app
# Install deps first (with an empty app/ dir) so this layer is cached
# until pyproject.toml changes, not every time code changes.
COPY backend/pyproject.toml ./
RUN mkdir app && pip install -e .
COPY backend/ ./

# ---- 3. Dev: adds test tools; code is bind-mounted by docker compose ----
FROM base AS dev
RUN pip install -e ".[dev]"
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --reload-dir app"]

# ---- 4. Prod: backend + built frontend in one image ----
FROM base AS prod
COPY --from=frontend-build /frontend/dist /app/static
RUN useradd --create-home --uid 1000 appuser
USER appuser
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
