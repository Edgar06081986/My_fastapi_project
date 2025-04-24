"""empty message

Revision ID: 8eb040eba589
Revises: 6cfcd6fcb054
Create Date: 2025-04-24 16:24:17.531532

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8eb040eba589'
down_revision: Union[str, None] = '6cfcd6fcb054'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
