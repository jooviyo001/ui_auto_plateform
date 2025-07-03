from pydantic import BaseModel, Field
from typing import List, Optional

class Step(BaseModel):
    action: str
    selector: Optional[str] = None
    url: Optional[str] = None
    text: Optional[str] = None

class Case(BaseModel):
    id: Optional[int] = Field(None, description="用例ID")
    name: str = Field(..., description="用例名称")
    project_id: int = Field(..., description="所属项目ID")
    group: Optional[str] = None
    description: Optional[str] = Field(None, description="用例描述")
    steps: List[Step] 