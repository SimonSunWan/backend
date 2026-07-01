from typing import List
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.department import DepartmentLeader


def is_super_admin(user: User) -> bool:
    """判断用户是否为超级管理员"""
    return any(role.role_code == "SUPER" for role in user.roles if role.status)


def is_department_leader(user: User, db: Session) -> bool:
    """判断用户是否为部门负责人"""
    return db.query(DepartmentLeader).filter(
        DepartmentLeader.user_id == user.id
    ).first() is not None


def get_department_member_ids(db: Session, user: User) -> List[int]:
    """获取用户负责的部门及其所有子部门下的成员ID列表"""
    from app.models.department import UserDepartment, Department
    
    # 获取用户负责的部门ID列表
    leading_dept_ids = [dept.id for dept in user.leading_departments if dept.status]
    
    if not leading_dept_ids:
        return []
    
    # 获取所有子部门的ID（递归查询）
    all_dept_ids = []
    
    # 使用递归函数获取所有子部门ID
    def get_all_child_dept_ids(parent_ids: List[int]):
        all_dept_ids.extend(parent_ids)
        
        # 查询这些部门下的所有直接子部门
        child_depts = db.query(Department.id).filter(
            Department.parent_id.in_(parent_ids),
            Department.status == True
        ).all()
        
        child_ids = [dept.id for dept in child_depts]
        if child_ids:
            get_all_child_dept_ids(child_ids)
    
    get_all_child_dept_ids(leading_dept_ids)
    
    # 获取这些部门下的所有成员ID
    user_ids = db.query(UserDepartment.user_id).filter(
        UserDepartment.dept_id.in_(all_dept_ids),
        UserDepartment.is_active == True
    ).all()
    
    # 获取所有成员ID，包括部门负责人自己
    member_ids = [user_id[0] for user_id in user_ids]
    
    # 确保包含当前用户自己的ID（因为部门负责人可能在查询中被遗漏）
    if user.id not in member_ids:
        member_ids.append(user.id)
    
    return member_ids
