from typing import Optional
import uuid
from sqlalchemy.orm import Session

from app.core.crud import CRUDBase
from app.models.repair_project import RepairProject
from app.schemas.repair_project import RepairProjectCreate, RepairProjectUpdate


class RepairProjectCRUD(CRUDBase):
    """维修项目CRUD操作"""

    def create(self, db: Session, *, obj_in: RepairProjectCreate, created_by: Optional[str] = None) -> RepairProject:
        """
        创建维修项目
        """
        # 生成ID
        obj_data = obj_in.dict()
        obj_data["id"] = str(uuid.uuid4()).replace("-", "")
        if created_by:
            obj_data["created_by"] = created_by
        
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: RepairProject, obj_in: RepairProjectUpdate, updated_by: Optional[str] = None
    ) -> RepairProject:
        """
        更新维修项目
        """
        update_data = obj_in.dict(exclude_unset=True)
        if updated_by:
            update_data["updated_by"] = updated_by
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# 创建CRUD实例
repair_project_crud = RepairProjectCRUD(RepairProject)