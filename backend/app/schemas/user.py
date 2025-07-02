from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    role: str = 'user'
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    id: int

class UserLogin(BaseModel):
    username: str
    password: str 