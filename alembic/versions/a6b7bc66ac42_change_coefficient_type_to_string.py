"""change_coefficient_type_to_string

Revision ID: a6b7bc66ac42
Revises: e3f60b4f7d25
Create Date: 2025-12-21 15:46:21.122071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6b7bc66ac42'
down_revision = 'e3f60b4f7d25'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 修改coefficient字段类型从Float到String
    op.alter_column('repair_project', 'coefficient',
                    existing_type=sa.Float(),
                    type_=sa.String(50),
                    existing_nullable=False)


def downgrade() -> None:
    # 将coefficient字段类型从String改回Float
    op.alter_column('repair_project', 'coefficient',
                    existing_type=sa.String(50),
                    type_=sa.Float(),
                    existing_nullable=False)
