from pydantic import BaseModel
from typing import List, Optional

class Step(BaseModel):
    action: str
    selector: Optional[str] = None
    url: Optional[str] = None
    text: Optional[str] = None

class Case(BaseModel):
    id: Optional[int] = None
    name: str
    project_id: int
    group: Optional[str] = None
    description: Optional[str] = None
    steps: List[Step] 