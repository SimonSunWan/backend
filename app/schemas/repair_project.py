from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.schemas.base import CamelCaseModel


class RepairProjectBase(BaseModel):
    """维修项目基础模型"""
    project_type: str = Field(..., description="项目类型")
    repair_project_code: str = Field(..., description="维修项目代码")
    fault_location_name: str = Field(..., description="故障位置")
    repair_project_name: str = Field(..., description="维修项目名称")
    coefficient: float = Field(..., description="工时系数")
    remark: Optional[str] = Field(None, description="备注")


class RepairProjectCreate(RepairProjectBase):
    """创建维修项目请求模型"""
    pass


class RepairProjectUpdate(BaseModel):
    """更新维修项目请求模型"""
    project_type: Optional[str] = Field(None, description="项目类型")
    repair_project_code: Optional[str] = Field(None, description="维修项目代码")
    fault_location_name: Optional[str] = Field(None, description="故障位置")
    repair_project_name: Optional[str] = Field(None, description="维修项目名称")
    coefficient: Optional[float] = Field(None, description="工时系数")
    remark: Optional[str] = Field(None, description="备注")


class RepairProjectResponse(RepairProjectBase, CamelCaseModel):
    """维修项目响应模型"""
    id: str = Field(..., description="ID")
    create_time: datetime = Field(..., description="创建时间")
    update_time: Optional[datetime] = Field(None, description="更新时间")
    created_by: Optional[str] = Field(None, description="创建者")
    updated_by: Optional[str] = Field(None, description="更新者")

    model_config = {"from_attributes": True}