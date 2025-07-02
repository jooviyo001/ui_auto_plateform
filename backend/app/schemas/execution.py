from pydantic import BaseModel
from typing import List, Optional

class BatchRunRequest(BaseModel):
    case_ids: List[int]

class CaseExecutionResult(BaseModel):
    case_id: int
    success: bool
    steps_result: Optional[List[str]] = None
    error: Optional[str] = None

class BatchRunResponse(BaseModel):
    results: List[CaseExecutionResult]

class AsyncBatchRunResponse(BaseModel):
    task_id: str

class TaskStatusResponse(BaseModel):
    status: str
    result: Optional[List[CaseExecutionResult]] = None 