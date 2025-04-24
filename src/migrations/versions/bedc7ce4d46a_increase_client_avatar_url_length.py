"""increase client_avatar_url length

Revision ID: bedc7ce4d46a
Revises: 9304a61d7a98
Create Date: 2025-04-23 16:54:35.677235

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bedc7ce4d46a"
down_revision: Union[str, None] = "9304a61d7a98"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "clients",
        "client_avatar_url",
        type_=sa.String(length=500),
        existing_type=sa.String(length=20),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "clients",
        "client_avatar_url",
        type_=sa.String(length=20),
        existing_type=sa.String(length=500),
    )
