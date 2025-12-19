"""add driver_deriver column to shipments

Revision ID: a6793b2ed768
Revises: 1b3d5f2851e9
Create Date: 2025-12-19 14:06:12.721849

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a6793b2ed768'
down_revision: Union[str, Sequence[str], None] = '1b3d5f2851e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "shipments",
        sa.Column("driver_deriver", sa.Integer, sa.ForeignKey("employee.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("shipments", "driver_deriver")
