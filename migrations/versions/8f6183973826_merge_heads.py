"""merge heads

Revision ID: 8f6183973826
Revises: 41f556c7cd31, 661c9d533972
Create Date: 2025-07-27 19:24:49.423268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8f6183973826'
down_revision: Union[str, None] = ('41f556c7cd31', '661c9d533972')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
