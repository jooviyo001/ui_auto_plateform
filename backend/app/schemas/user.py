from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., description="用户名")
    role: str = Field('user', description="用户角色（superadmin, admin, user）")
    is_active: bool = Field(True, description="是否激活")

class UserCreate(UserBase):
    password: str = Field(..., description="密码")

class UserOut(UserBase):
    id: int = Field(..., description="用户ID")

class UserLogin(BaseModel):
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码") 