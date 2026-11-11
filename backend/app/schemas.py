"""API response shapes. Kept separate from ORM models so the DB and the API can evolve independently."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models import EventSource


class EventOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # allows building from an ORM object

    id: int
    source: EventSource
    external_id: str
    title: str
    start_at: datetime
    end_at: datetime
    all_day: bool
    updated_at: datetime


class HealthOut(BaseModel):
    status: str
