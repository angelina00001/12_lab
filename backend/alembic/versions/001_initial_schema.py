"""initial schema — rooms, guests, bookings, stays, cleaning (задание 7)

Revision ID: 001
Revises:
Create Date: 2026-05-15
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)

    op.create_table(
        "rooms",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("number", sa.String(20), nullable=False),
        sa.Column("room_type", sa.String(20), nullable=False),
        sa.Column("price_per_night", sa.Float(), nullable=False),
        sa.Column("capacity", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("floor", sa.Integer()),
        sa.Column("description", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_rooms_id", "rooms", ["id"])
    op.create_index("ix_rooms_number", "rooms", ["number"], unique=True)
    op.create_index("ix_rooms_status", "rooms", ["status"])

    op.create_table(
        "guests",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("email", sa.String(255)),
        sa.Column("phone", sa.String(30)),
        sa.Column("document_id", sa.String(50)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_guests_email", "guests", ["email"])

    op.create_table(
        "bookings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("guest_id", sa.Integer(), sa.ForeignKey("guests.id"), nullable=False),
        sa.Column("created_by_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("check_in", sa.Date(), nullable=False),
        sa.Column("check_out", sa.Date(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("notes", sa.String(500)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_bookings_room_id", "bookings", ["room_id"])
    op.create_index("ix_bookings_guest_id", "bookings", ["guest_id"])
    op.create_index("ix_bookings_check_in", "bookings", ["check_in"])
    op.create_index("ix_bookings_status", "bookings", ["status"])

    op.create_table(
        "stays",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("booking_id", sa.Integer(), sa.ForeignKey("bookings.id"), nullable=False),
        sa.Column("actual_check_in", sa.DateTime(timezone=True)),
        sa.Column("actual_check_out", sa.DateTime(timezone=True)),
        sa.Column("status", sa.String(20), nullable=False),
    )
    op.create_index("ix_stays_booking_id", "stays", ["booking_id"], unique=True)

    op.create_table(
        "cleaning_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("room_id", sa.Integer(), sa.ForeignKey("rooms.id"), nullable=False),
        sa.Column("assigned_to_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("scheduled_at", sa.DateTime(timezone=True)),
        sa.Column("completed_at", sa.DateTime(timezone=True)),
        sa.Column("notes", sa.String(500)),
    )
    op.create_index("ix_cleaning_room_id", "cleaning_tasks", ["room_id"])
    op.create_index("ix_cleaning_status", "cleaning_tasks", ["status"])


def downgrade() -> None:
    op.drop_table("cleaning_tasks")
    op.drop_table("stays")
    op.drop_table("bookings")
    op.drop_table("guests")
    op.drop_table("rooms")
    op.drop_table("users")
