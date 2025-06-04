from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision = "e9b7db34ec77"
down_revision = "553d253d36da"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Сначала явно создаём тип workload
    op.execute(
        """
    CREATE TYPE workload AS ENUM (
        'repair', 
        'production', 
        'production_and_repair'
    )
    """
    )

    # Затем изменяем столбцы
    op.alter_column(
        "jewelers",
        "workload",
        existing_type=sa.VARCHAR(length=21),
        type_=sa.Enum("repair", "production", "production_and_repair", name="workload"),
        postgresql_using="workload::workload",
        existing_nullable=False,
    )
    op.alter_column(
        "orders",
        "workload",
        existing_type=sa.VARCHAR(length=21),
        type_=sa.Enum("repair", "production", "production_and_repair", name="workload"),
        postgresql_using="workload::workload",
        existing_nullable=False,
    )


def downgrade() -> None:
    # Возвращаем VARCHAR тип
    op.alter_column(
        "orders",
        "workload",
        existing_type=sa.Enum(
            "repair", "production", "production_and_repair", name="workload"
        ),
        type_=sa.VARCHAR(length=21),
        postgresql_using="workload::text",
        existing_nullable=False,
    )
    op.alter_column(
        "jewelers",
        "workload",
        existing_type=sa.Enum(
            "repair", "production", "production_and_repair", name="workload"
        ),
        type_=sa.VARCHAR(length=21),
        postgresql_using="workload::text",
        existing_nullable=False,
    )

    # Удаляем тип только после изменения всех столбцов
    op.execute("DROP TYPE workload")

    # Убираем создание spatial_ref_sys - это системная таблица PostGIS
    # op.create_table("spatial_ref_sys", ...)  # Закомментируйте эту часть
