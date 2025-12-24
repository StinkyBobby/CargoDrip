"""restore driver_deriver column

Revision ID: 09dedf4dac42
Revises: ad651dbb0f08
Create Date: 2025-12-24 01:01:25.647439

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '09dedf4dac42'
down_revision: Union[str, Sequence[str], None] = 'ad651dbb0f08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # вернуть колонку driver_deriver
    op.add_column(
        "shipments",
        sa.Column("driver_deriver", sa.Integer(), nullable=False)
    )


def downgrade():
    # удалить колонку driver_deriver
    op.drop_column("shipments", "driver_deriver")
