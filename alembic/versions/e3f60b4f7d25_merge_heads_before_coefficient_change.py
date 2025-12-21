"""merge_heads_before_coefficient_change

Revision ID: e3f60b4f7d25
Revises: 006_add_proj_type_ext_order, 007_add_repair_project_table, add_avic_order_number
Create Date: 2025-12-21 15:46:06.092439

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e3f60b4f7d25'
down_revision = ('006_add_proj_type_ext_order', '007_add_repair_project_table', 'add_avic_order_number')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
