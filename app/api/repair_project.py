from typing import List, Optional
from fastapi import APIRouter, Body, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_active_user
from app.crud import repair_project_crud
from app.models.user import User
from app.models.repair_project import RepairProject
from app.schemas.base import ApiResponse, PaginatedResponse
from app.schemas.repair_project import RepairProjectCreate, RepairProjectResponse, RepairProjectUpdate

router = APIRouter()


@router.get("/list", response_model=ApiResponse[PaginatedResponse[RepairProjectResponse]])
def get_repair_projects(
    current: int = Query(1, ge=1, description="当前页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    projectType: Optional[str] = Query(None, description="项目类型"),
    faultLocation: Optional[str] = Query(None, description="故障位置"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """获取维修项目列表"""
    try:
        skip = (current - 1) * size

        # 构建查询
        query = db.query(RepairProject)

        # 添加筛选条件
        if projectType:
            query = query.filter(RepairProject.project_type == projectType)

        if faultLocation:
            query = query.filter(RepairProject.fault_location_name == faultLocation)

        # 获取总数
        total = query.count()

        # 按创建时间倒序排序并获取分页数据
        repair_projects = (
            query.order_by(RepairProject.create_time.desc())
            .offset(skip)
            .limit(size)
            .all()
        )

        # 将 SQLAlchemy 对象转换为普通字典，交给 Pydantic 做二次校验
        records = []
        for rp in repair_projects:
            records.append(
                {
                    "id": rp.id,
                    "project_type": rp.project_type,
                    "repair_project_code": rp.repair_project_code,
                    "fault_location_name": rp.fault_location_name,
                    "repair_project_name": rp.repair_project_name,
                    "coefficient": rp.coefficient,
                    "remark": rp.remark,
                    "create_time": rp.create_time,
                    "update_time": rp.update_time,
                    "created_by": rp.created_by,
                    "updated_by": rp.updated_by,
                }
            )

        # 构建分页响应数据
        response_data = {
            "records": records,
            "total": total,
            "current": current,
            "size": size,
        }

        return ApiResponse(data=response_data, message="获取维修项目列表成功")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取维修项目列表失败: {str(e)}")


@router.get("/{repair_project_id}", response_model=ApiResponse[RepairProjectResponse])
def get_repair_project(
    repair_project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """根据ID获取维修项目"""
    repair_project = repair_project_crud.get(db, id=repair_project_id)
    if not repair_project:
        raise HTTPException(status_code=404, detail="维修项目不存在")
    
    # 转换SQLAlchemy模型为Pydantic模型
    return ApiResponse(data=RepairProjectResponse.model_validate(repair_project), message="获取维修项目成功")


@router.post("/", response_model=ApiResponse[RepairProjectResponse])
def create_repair_project(
    repair_project: RepairProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """创建维修项目"""
    # 检查维修项目代码是否已存在
    existing_project = db.query(RepairProject).filter(
        RepairProject.repair_project_code == repair_project.repair_project_code
    ).first()
    
    if existing_project:
        raise HTTPException(status_code=400, detail="维修项目代码已存在")
    
    # 创建维修项目
    db_repair_project = repair_project_crud.create(
        db, obj_in=repair_project, created_by=current_user.user_name
    )
    
    # 转换SQLAlchemy模型为Pydantic模型
    return ApiResponse(
        data=RepairProjectResponse.model_validate(db_repair_project), 
        message="创建维修项目成功"
    )


@router.put("/{repair_project_id}", response_model=ApiResponse[RepairProjectResponse])
def update_repair_project(
    repair_project_id: str,
    repair_project_update: RepairProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """更新维修项目"""
    db_repair_project = repair_project_crud.get(db, id=repair_project_id)
    if not db_repair_project:
        raise HTTPException(status_code=404, detail="维修项目不存在")
    
    # 如果更新了维修项目代码，检查是否与其他项目重复
    if repair_project_update.repair_project_code and \
       repair_project_update.repair_project_code != db_repair_project.repair_project_code:
        existing_project = db.query(RepairProject).filter(
            RepairProject.repair_project_code == repair_project_update.repair_project_code,
            RepairProject.id != repair_project_id
        ).first()
        
        if existing_project:
            raise HTTPException(status_code=400, detail="维修项目代码已存在")
    
    # 更新维修项目
    updated_repair_project = repair_project_crud.update(
        db, db_obj=db_repair_project, obj_in=repair_project_update, updated_by=current_user.user_name
    )
    
    # 转换SQLAlchemy模型为Pydantic模型
    return ApiResponse(
        data=RepairProjectResponse.model_validate(updated_repair_project), 
        message="更新维修项目成功"
    )


@router.delete("/{repair_project_id}", response_model=ApiResponse[dict])
def delete_repair_project(
    repair_project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """删除维修项目"""
    try:
        db_repair_project = repair_project_crud.get(db, id=repair_project_id)
        if not db_repair_project:
            raise HTTPException(status_code=404, detail="维修项目不存在")
        
        repair_project_crud.remove(db, id=repair_project_id)
        
        return ApiResponse(message="删除维修项目成功")
    except HTTPException:
        raise  # 重新抛出HTTPException
    except Exception as e:
        # 捕获其他异常并返回500错误
        db.rollback()
        raise HTTPException(status_code=500, detail=f"删除维修项目失败: {str(e)}")


@router.delete("/batch", response_model=ApiResponse[dict])
def batch_delete_repair_projects(
    ids: List[str] = Body(..., embed=True, description="要删除的维修项目ID列表"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """批量删除维修项目"""
    try:
        if not ids:
            raise HTTPException(status_code=400, detail="请提供要删除的维修项目ID列表")
        
        # 检查所有项目是否存在
        existing_projects = db.query(RepairProject).filter(RepairProject.id.in_(ids)).all()
        if len(existing_projects) != len(ids):
            raise HTTPException(status_code=404, detail="部分维修项目不存在")
        
        # 批量删除
        db.query(RepairProject).filter(RepairProject.id.in_(ids)).delete(synchronize_session=False)
        db.commit()
        
        return ApiResponse(message=f"批量删除维修项目成功，共删除{len(ids)}个")
    except HTTPException:
        raise  # 重新抛出HTTPException
    except Exception as e:
        # 捕获其他异常并返回500错误
        db.rollback()
        raise HTTPException(status_code=500, detail=f"批量删除维修项目失败: {str(e)}")


@router.get("/export", response_class=StreamingResponse)
def export_repair_projects(
    projectType: Optional[str] = Query(None, description="项目类型"),
    faultLocation: Optional[str] = Query(None, description="故障位置"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
):
    """导出维修项目列表"""
    # 构建查询
    query = db.query(RepairProject)
    
    # 添加筛选条件
    if projectType:
        query = query.filter(RepairProject.project_type == projectType)
    
    if faultLocation:
        query = query.filter(RepairProject.fault_location_name == faultLocation)
    
    # 获取所有数据
    repair_projects = query.order_by(RepairProject.create_time.desc()).all()
    
    # 这里可以实现导出逻辑，例如导出为Excel
    # 简化示例，实际应用中可以使用pandas或其他库实现Excel导出
    import io
    import csv
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入标题行
    writer.writerow([
        "ID", "项目类型", "维修项目代码", "故障位置", "维修项目名称", "工时系数", "备注", "创建时间", "更新时间"
    ])
    
    # 写入数据行
    for project in repair_projects:
        writer.writerow([
            project.id,
            project.project_type,
            project.repair_project_code,
            project.fault_location_name,
            project.repair_project_name,
            project.coefficient,
            project.remark,
            project.create_time.strftime("%Y-%m-%d %H:%M:%S") if project.create_time else "",
            project.update_time.strftime("%Y-%m-%d %H:%M:%S") if project.update_time else ""
        ])
    
    output.seek(0)
    
    # 返回CSV文件
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8-sig")),  # 使用utf-8-sig支持中文
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=repair_projects.csv"}
    )