from pydantic import BaseModel, Field
from typing import Optional

class Setting(BaseModel):
    id: Optional[int] = Field(None, description="设置ID")
    key: str = Field(..., description="设置项Key")
    value: str = Field(..., description="设置项Value")
    type: str = 'string'
    group: str = 'general'
    description: Optional[str] = Field(None, description="设置项描述")

class SettingOut(Setting):
    pass 