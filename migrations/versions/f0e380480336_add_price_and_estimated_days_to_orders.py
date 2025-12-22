"""add price and estimated_days to orders

Revision ID: f0e380480336
Revises: a6793b2ed768
Create Date: 2025-12-22 11:50:15.108206

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f0e380480336'
down_revision: Union[str, Sequence[str], None] = 'a6793b2ed768'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column("orders", sa.Column("price", sa.Float(), nullable=False, server_default="0"))
    op.add_column("orders", sa.Column("estimated_days", sa.Integer(), nullable=False, server_default="1"))



def downgrade() -> None:
    """Downgrade schema."""
    pass
