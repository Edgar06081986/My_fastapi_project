"""revert_problematic_changes

Revision ID: 716bf267f844
Revises: 60519016b922
Create Date: 2025-04-23 10:36:10.518379

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "716bf267f844"
down_revision: Union[str, None] = "60519016b922"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
