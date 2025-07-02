from pydantic import BaseModel
from typing import Optional

class SettingBase(BaseModel):
    key: str
    value: str
    type: str = 'string'
    group: str = 'general'
    description: Optional[str] = None

class SettingOut(SettingBase):
    id: int 