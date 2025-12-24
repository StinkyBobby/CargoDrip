"""rename driver_deriver to driver_id

Revision ID: ad651dbb0f08
Revises: ad3a61e7ef27
Create Date: 2025-12-24 00:57:35.887582

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad651dbb0f08'
down_revision: Union[str, Sequence[str], None] = 'ad3a61e7ef27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Переименовать колонку
    op.alter_column(
        "shipments",
        "driver_deriver",
        new_column_name="driver_id",
        existing_type=sa.Integer(),
        nullable=True,   # разрешаем NULL
    )


def downgrade():
    # Вернуть обратно
    op.alter_column(
        "shipments",
        "driver_id",
        new_column_name="driver_deriver",
        existing_type=sa.Integer(),
        nullable=False,  # как было раньше
    )
