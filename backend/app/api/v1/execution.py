from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.schemas.execution import BatchRunRequest, BatchRunResponse, CaseExecutionResult, AsyncBatchRunResponse, TaskStatusResponse, Execution
from app.services.drission_executor import DrissionExecutor
from app.services.case_service import CaseService
from app.schemas.case import Step
from app.services.execution_service import ExecutionService
from app.tasks.execution_tasks import batch_run_cases_task
from celery.result import AsyncResult
import json
from app.utils.response import success, fail
from app.schemas.common import ResponseModel

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post('/batch_run', response_model=BatchRunResponse)
def batch_run_cases(req: BatchRunRequest, db: Session = Depends(get_db)):
    results = []
    for case_id in req.case_ids:
        db_case = CaseService.get_case(db, case_id)
        if not db_case:
            results.append(CaseExecutionResult(case_id=case_id, success=False, error="用例不存在"))
            continue
        try:
            steps = [Step(**step) for step in json.loads(db_case.steps)]
            executor = DrissionExecutor()
            step_dicts = [step.dict() for step in steps]
            step_results = executor.run_steps(step_dicts)
            results.append(CaseExecutionResult(case_id=case_id, success=True, steps_result=step_results))
        except Exception as e:
            results.append(CaseExecutionResult(case_id=case_id, success=False, error=str(e)))
    return BatchRunResponse(results=results)

@router.post('/async_batch_run', response_model=AsyncBatchRunResponse)
def async_batch_run_cases(req: BatchRunRequest, db: Session = Depends(get_db)):
    celery_task = batch_run_cases_task.apply_async(args=[req.case_ids])
    ExecutionService.create_task(db, celery_task.id, req.case_ids)
    return AsyncBatchRunResponse(task_id=celery_task.id)

@router.get('/task_status/{task_id}', response_model=TaskStatusResponse)
def get_task_status(task_id: str, db: Session = Depends(get_db)):
    celery_result = AsyncResult(task_id)
    db_task = ExecutionService.get_task_by_celery_id(db, task_id)
    status = celery_result.status
    result = None
    if celery_result.successful():
        try:
            result = [CaseExecutionResult(**r) for r in celery_result.result]
        except Exception:
            result = None
    return TaskStatusResponse(status=status, result=result)

@router.get('/history', response_model=list)
def get_execution_history(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    tasks = ExecutionService.list_tasks(db, skip, limit)
    return [
        {
            'id': t.id,
            'task_id': t.celery_task_id,
            'status': t.status,
            'case_ids': json.loads(t.case_ids),
            'result': json.loads(t.result) if t.result else None,
            'start_time': t.start_time,
            'end_time': t.end_time
        } for t in tasks
    ]

@router.get('/', response_model=ResponseModel)
def get_executions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    data = ExecutionService.get_executions(db, skip, limit)
    return success(data)

@router.post('/', response_model=ResponseModel)
def create_execution(execution: Execution, db: Session = Depends(get_db)):
    data = ExecutionService.create_execution(db, execution)
    return success(data, msg="创建成功")

@router.get('/{execution_id}', response_model=ResponseModel)
def get_execution(execution_id: int, db: Session = Depends(get_db)):
    data = ExecutionService.get_execution(db, execution_id)
    if not data:
        return fail("执行记录不存在", code=404)
    return success(data)

@router.put('/{execution_id}', response_model=ResponseModel)
def update_execution(execution_id: int, execution: Execution, db: Session = Depends(get_db)):
    data = ExecutionService.update_execution(db, execution_id, execution)
    if not data:
        return fail("执行记录不存在", code=404)
    return success(data, msg="更新成功")

@router.delete('/{execution_id}', response_model=ResponseModel)
def delete_execution(execution_id: int, db: Session = Depends(get_db)):
    data = ExecutionService.delete_execution(db, execution_id)
    if not data:
        return fail("执行记录不存在", code=404)
    return success(data, msg="删除成功") 