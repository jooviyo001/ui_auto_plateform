from pydantic import BaseModel, Field
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

class Execution(BaseModel):
    id: Optional[int] = Field(None, description="执行ID")
    case_id: int = Field(..., description="用例ID")
    status: str = Field(..., description="执行状态")
    result: Optional[str] = Field(None, description="执行结果")
    start_time: Optional[str] = Field(None, description="开始时间")
    end_time: Optional[str] = Field(None, description="结束时间") 