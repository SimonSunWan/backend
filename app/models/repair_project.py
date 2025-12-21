from sqlalchemy import Column, Float, String, Text

from app.core.database import Base
from app.models.base import TimestampMixin


class RepairProject(Base, TimestampMixin):
    """维修项目模型"""

    __tablename__ = "repair_project"

    id = Column(String, primary_key=True, index=True)
    project_type = Column(String(50), nullable=False, comment="项目类型")
    repair_project_code = Column(String(100), nullable=False, comment="维修项目代码")
    fault_location_name = Column(String(50), nullable=False, comment="故障位置")
    repair_project_name = Column(String(200), nullable=False, comment="维修项目名称")
    coefficient = Column(String(50), nullable=False, comment="工时系数")
    remark = Column(Text, comment="备注")