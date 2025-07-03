from pydantic import BaseModel
from typing import Any, Optional

class ResponseModel(BaseModel):
    code: int = 0
    msg: str = "成功"
    data: Optional[Any] = None 