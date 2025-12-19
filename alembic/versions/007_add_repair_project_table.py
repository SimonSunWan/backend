"""Add repair project table

Revision ID: 007_add_repair_project_table
Revises: 005_add_department_tables
Create Date: 2025-12-17 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '007_add_repair_project_table'
down_revision = '005_add_department_tables'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """创建维修项目表"""
    op.create_table(
        'repair_project',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('project_type', sa.String(50), nullable=False, comment='项目类型'),
        sa.Column('repair_project_code', sa.String(100), nullable=False, comment='维修项目代码'),
        sa.Column('fault_location_name', sa.String(50), nullable=False, comment='故障位置'),
        sa.Column('repair_project_name', sa.String(200), nullable=False, comment='维修项目名称'),
        sa.Column('coefficient', sa.Float(), nullable=False, comment='工时系数'),
        sa.Column('remark', sa.Text(), nullable=True, comment='备注'),
        sa.Column('create_time', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True, comment='创建时间'),
        sa.Column('update_time', sa.DateTime(timezone=True), nullable=True, comment='更新时间'),
        sa.Column('created_by', sa.String(100), nullable=True, comment='创建者'),
        sa.Column('updated_by', sa.String(100), nullable=True, comment='更新者'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # 创建索引
    op.create_index(op.f('ix_repair_project_id'), 'repair_project', ['id'], unique=False)
    op.create_index(op.f('ix_repair_project_repair_project_code'), 'repair_project', ['repair_project_code'], unique=True)
    op.create_index(op.f('ix_repair_project_project_type'), 'repair_project', ['project_type'], unique=False)
    op.create_index(op.f('ix_repair_project_fault_location_name'), 'repair_project', ['fault_location_name'], unique=False)


def downgrade() -> None:
    """删除维修项目表"""
    op.drop_index(op.f('ix_repair_project_fault_location_name'), table_name='repair_project')
    op.drop_index(op.f('ix_repair_project_project_type'), table_name='repair_project')
    op.drop_index(op.f('ix_repair_project_repair_project_code'), table_name='repair_project')
    op.drop_index(op.f('ix_repair_project_id'), table_name='repair_project')
    op.drop_table('repair_project')