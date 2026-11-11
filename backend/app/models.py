"""ORM models: Python classes that map to database tables."""

import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class EventSource(str, enum.Enum):
    google = "google"
    outlook = "outlook"


class Event(Base):
    __tablename__ = "events"
    # The same calendar event must never be stored twice for one source.
    __table_args__ = (
        UniqueConstraint("source", "external_id", name="uq_events_source_external_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[EventSource] = mapped_column(Enum(EventSource, name="event_source"))
    external_id: Mapped[str] = mapped_column(String(1024))  # the event's ID in Google/Outlook
    title: Mapped[str] = mapped_column(String(1024))
    start_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    end_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    all_day: Mapped[bool] = mapped_column(default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
