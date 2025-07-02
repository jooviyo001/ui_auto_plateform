from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import Project
from app.services.project_service import ProjectService
from app.core.database import SessionLocal
from typing import List

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/', response_model=Project)
def create_project(project: Project, db: Session = Depends(get_db)):
    return ProjectService.create_project(db, project)

@router.get('/{project_id}', response_model=Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = ProjectService.get_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project

@router.get('/', response_model=List[Project])
def get_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ProjectService.get_projects(db, skip, limit)

@router.put('/{project_id}', response_model=Project)
def update_project(project_id: int, project: Project, db: Session = Depends(get_db)):
    db_project = ProjectService.update_project(db, project_id, project)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project

@router.delete('/{project_id}', response_model=Project)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    db_project = ProjectService.delete_project(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="项目不存在")
    return db_project 