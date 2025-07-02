from app.models.project import Project, Base
from app.schemas.project import Project as ProjectSchema
from sqlalchemy.orm import Session

class ProjectService:
    @staticmethod
    def create_project(db: Session, project: ProjectSchema):
        db_project = Project(name=project.name, description=project.description, owner=project.owner)
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def get_project(db: Session, project_id: int):
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_projects(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Project).offset(skip).limit(limit).all()

    @staticmethod
    def update_project(db: Session, project_id: int, project: ProjectSchema):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        db_project.name = project.name
        db_project.description = project.description
        db_project.owner = project.owner
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int):
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        db.delete(db_project)
        db.commit()
        return db_project 