"""add orders table

Revision ID: 1b3d5f2851e9
Revises: 3253f8054eca
Create Date: 2025-12-19 13:42:25.002511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b3d5f2851e9'
down_revision: Union[str, Sequence[str], None] = '3253f8054eca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("cargo_id", sa.Integer, sa.ForeignKey("cargoes.id"), nullable=False),
        sa.Column("to_location", sa.String(length=255), nullable=False),
        sa.Column("distance_km", sa.Integer, nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime,
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "status",
            sa.Enum("queued", "assigned", "completed", name="orderstatus"),
            nullable=False,
            server_default="queued",
        ),
        sa.Column("truck_id", sa.Integer, sa.ForeignKey("trucks.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("orders")
    op.execute("DROP TYPE IF EXISTS orderstatus")
