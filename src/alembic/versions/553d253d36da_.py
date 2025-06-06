"""empty message

Revision ID: 553d253d36da
Revises:
Create Date: 2025-04-25 09:18:01.196693

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "553d253d36da"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "clients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(length=30), nullable=False),
        sa.Column("client_avatar_url", sa.String(length=500), nullable=True),
        sa.Column("phone_number", sa.String(length=30), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "jewelers",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("email", sa.String(length=30), nullable=False),
        sa.Column(
            "workload",
            sa.Enum(
                "repair",
                "production",
                "production_and_repair",
                name="workload",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("portfolio", sa.String(length=500), nullable=True),
        sa.Column("jeweler_avatar_url", sa.String(length=500), nullable=True),
        sa.Column("phone_number", sa.String(length=30), nullable=False),
        sa.Column("address", sa.String(length=256), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "m2m_jewelers_clients",
        sa.Column("jeweler_id", sa.Integer(), nullable=False),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.Column("cover_letter", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["jeweler_id"], ["jewelers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("jeweler_id", "client_id"),
    )
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=256), nullable=False),
        sa.Column("order_avatar_url", sa.String(length=500), nullable=True),
        sa.Column(
            "workload",
            sa.Enum(
                "repair",
                "production",
                "production_and_repair",
                name="workload",
                native_enum=False,
            ),
            nullable=False,
        ),
        sa.Column("compensation", sa.Integer(), nullable=True),
        sa.Column("jeweler_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now())"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.text("TIMEZONE('utc', now()+ interval '1 day')"),
            nullable=False,
        ),
        sa.Column("client_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["client_id"], ["clients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["jeweler_id"],
            ["jewelers.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("orders")
    op.drop_table("m2m_jewelers_clients")
    op.drop_table("jewelers")
    op.drop_table("clients")
    op.execute("DROP TYPE IF EXISTS workload CASCADE")
    # ### end Alembic commands ###
