from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import Project
from app.services.project_service import ProjectService
from app.core.database import SessionLocal
from typing import List
from app.utils.response import success, fail
from app.schemas.common import ResponseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=ResponseModel)
def create_project(project: Project, db: Session = Depends(get_db)):
    data = ProjectService.create_project(db, project)
    return success(data, msg="创建成功")

@router.get('/{project_id}', response_model=ResponseModel)
def get_project(project_id: int, db: Session = Depends(get_db)):
    data = ProjectService.get_project(db, project_id)
    if not data:
        return fail("项目不存在", code=404)
    return success(data)

@router.get('/', response_model=ResponseModel)
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ProjectService.get_projects(db, skip, limit)
    return success(data)

@router.put('/{project_id}', response_model=ResponseModel)
def update_project(project_id: int, project: Project, db: Session = Depends(get_db)):
    data = ProjectService.update_project(db, project_id, project)
    if not data:
        return fail("项目不存在", code=404)
    return success(data, msg="更新成功")

@router.delete('/{project_id}', response_model=ResponseModel)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    data = ProjectService.delete_project(db, project_id)
    if not data:
        return fail("项目不存在", code=404)
    return success(data, msg="删除成功") 