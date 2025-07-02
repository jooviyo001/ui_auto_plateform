from app.models.execution import ExecutionTask, ExecutionResult, Base
from sqlalchemy.orm import Session
import json, datetime

class ExecutionService:
    @staticmethod
    def create_task(db: Session, celery_task_id: str, case_ids: list):
        db_task = ExecutionTask(
            celery_task_id=celery_task_id,
            status='PENDING',
            case_ids=json.dumps(case_ids),
            start_time=datetime.datetime.utcnow()
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def update_task_status(db: Session, celery_task_id: str, status: str, result=None, end_time=None):
        db_task = db.query(ExecutionTask).filter(ExecutionTask.celery_task_id == celery_task_id).first()
        if db_task:
            db_task.status = status
            if result is not None:
                db_task.result = json.dumps(result)
            if end_time:
                db_task.end_time = end_time
            db.commit()
            db.refresh(db_task)
        return db_task

    @staticmethod
    def get_task_by_celery_id(db: Session, celery_task_id: str):
        return db.query(ExecutionTask).filter(ExecutionTask.celery_task_id == celery_task_id).first()

    @staticmethod
    def get_task_by_id(db: Session, task_id: int):
        return db.query(ExecutionTask).filter(ExecutionTask.id == task_id).first()

    @staticmethod
    def list_tasks(db: Session, skip=0, limit=20):
        return db.query(ExecutionTask).order_by(ExecutionTask.start_time.desc()).offset(skip).limit(limit).all() 