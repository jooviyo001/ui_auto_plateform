from pydantic import BaseModel
from typing import Optional
 
class Project(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    owner: Optional[str] = None 