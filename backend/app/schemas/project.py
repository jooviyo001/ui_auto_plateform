from pydantic import BaseModel, Field
from typing import Optional
 
class Project(BaseModel):
    id: Optional[int] = Field(None, description="项目ID")
    name: str = Field(..., description="项目名称")
    description: Optional[str] = Field(None, description="项目描述")
    owner: Optional[str] = Field(None, description="项目负责人") 