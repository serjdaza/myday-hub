"""FastAPI entry point: API routes under /api, plus the built React app at /."""

import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api import events, health
from app.config import get_settings

app = FastAPI(title="myday-hub")

app.include_router(health.router, prefix="/api")
app.include_router(events.router, prefix="/api")

# In the prod image the React build is copied to static_dir. In dev it doesn't
# exist (Vite serves the frontend instead), so only mount it when present.
# Mounted last so it never shadows /api routes.
_static_dir = get_settings().static_dir
if os.path.isdir(_static_dir):
    app.mount("/", StaticFiles(directory=_static_dir, html=True), name="static")
