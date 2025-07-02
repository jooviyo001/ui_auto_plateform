from app.models.case import Case, Base
from app.schemas.case import Case as CaseSchema
from sqlalchemy.orm import Session
import json

class CaseService:
    @staticmethod
    def create_case(db: Session, case: CaseSchema):
        db_case = Case(
            name=case.name,
            project_id=case.project_id,
            group=case.group,
            description=case.description,
            steps=json.dumps([step.dict() for step in case.steps])
        )
        db.add(db_case)
        db.commit()
        db.refresh(db_case)
        return db_case

    @staticmethod
    def get_case(db: Session, case_id: int):
        db_case = db.query(Case).filter(Case.id == case_id).first()
        return db_case

    @staticmethod
    def get_cases(db: Session, project_id: int = None, skip: int = 0, limit: int = 100):
        query = db.query(Case)
        if project_id:
            query = query.filter(Case.project_id == project_id)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def update_case(db: Session, case_id: int, case: CaseSchema):
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return None
        db_case.name = case.name
        db_case.project_id = case.project_id
        db_case.group = case.group
        db_case.description = case.description
        db_case.steps = json.dumps([step.dict() for step in case.steps])
        db.commit()
        db.refresh(db_case)
        return db_case

    @staticmethod
    def delete_case(db: Session, case_id: int):
        db_case = db.query(Case).filter(Case.id == case_id).first()
        if not db_case:
            return None
        db.delete(db_case)
        db.commit()
        return db_case 