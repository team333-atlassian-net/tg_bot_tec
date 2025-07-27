"""merge heads

Revision ID: 41f556c7cd31
Revises: 87e3128da0fb, b165bb786989
Create Date: 2025-07-27 13:04:38.288094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41f556c7cd31'
down_revision: Union[str, None] = ('87e3128da0fb', 'b165bb786989')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
