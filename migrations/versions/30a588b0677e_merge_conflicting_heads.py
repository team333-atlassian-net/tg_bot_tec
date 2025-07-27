"""Merge conflicting heads

Revision ID: 30a588b0677e
Revises: 87e3128da0fb, b165bb786989
Create Date: 2025-07-26 21:16:06.778467

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '30a588b0677e'
down_revision: Union[str, None] = ('87e3128da0fb', 'b165bb786989')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
