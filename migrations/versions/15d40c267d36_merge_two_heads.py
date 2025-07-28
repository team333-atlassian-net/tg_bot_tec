"""merge two heads

Revision ID: 15d40c267d36
Revises: 744d273f0b19, 8f6183973826
Create Date: 2025-07-28 11:19:37.047013

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '15d40c267d36'
down_revision: Union[str, None] = ('744d273f0b19', '8f6183973826')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
