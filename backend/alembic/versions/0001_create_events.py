"""create events table

Revision ID: 0001
Revises:
"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "events",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source", sa.Enum("google", "outlook", name="event_source"), nullable=False),
        sa.Column("external_id", sa.String(1024), nullable=False),
        sa.Column("title", sa.String(1024), nullable=False),
        sa.Column("start_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("end_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("all_day", sa.Boolean(), nullable=False),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.UniqueConstraint("source", "external_id", name="uq_events_source_external_id"),
    )
    op.create_index("ix_events_start_at", "events", ["start_at"])


def downgrade() -> None:
    op.drop_index("ix_events_start_at", table_name="events")
    op.drop_table("events")
    sa.Enum(name="event_source").drop(op.get_bind())
