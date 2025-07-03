from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from app.core.database import SessionLocal
from app.schemas.user import UserLogin, UserCreate, UserOut
from app.services.user_service import UserService
from app.core.jwt_auth import create_access_token, verify_access_token
from app.models.user import User
from typing import List, cast, Callable
from app.utils.response import fail, success
from app.services.user_service import pwd_context

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

# 权限依赖
ROLE_SUPERADMIN = 'superadmin'
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

def require_roles(*required_roles: str) -> Callable:
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in required_roles:
            raise HTTPException(status_code=403, detail="无权限")
        return current_user
    return role_checker


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="无效token")
    username = payload.get('sub', '')
    if not isinstance(username, str):
        raise HTTPException(status_code=401, detail="无效token")
    user = UserService.get_user_by_username(db, username)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户不存在或已禁用")
    return cast(User, user)

@router.post("/login")
def login_for_access_token(user_login: UserLogin, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, user_login.username, user_login.password)
    if not user:
        return fail(msg="用户名或密码错误")
    access_token = create_access_token(data={"sub": user.username})
    return success(data={"access_token": access_token, "token_type": "bearer"})

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已存在")
    return UserService.create_user(db, user)

@router.get("/users", response_model=List[UserOut])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    if current.role != ROLE_SUPERADMIN:  # 使用!=代替is_方法
        raise HTTPException(status_code=403, detail="无权限")
    return UserService.get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可查看任意用户，普通用户只能查看自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:  # 使用!=代替is_方法
        raise HTTPException(status_code=403, detail="无权限")
    return db_user

@router.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可编辑任意用户，普通用户只能编辑自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:  # 使用!=代替is_方法
        raise HTTPException(status_code=403, detail="无权限")
    db_user.username = user.username
    if current.role == ROLE_SUPERADMIN:  # 使用==代替is_方法
        db_user.role = user.role
    if user.password:
        db_user.hashed_password = pwd_context.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可删除任意用户，普通用户只能删除自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:  # 使用!=代替is_方法
        raise HTTPException(status_code=403, detail="无权限")
    db.delete(db_user)
    db.commit()
    return db_user

@router.post("/users/{user_id}/reset-password")
def reset_password(user_id: int, password: str, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可重置任意用户，普通用户只能重置自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:
        raise HTTPException(status_code=403, detail="无权限")
    db_user.hashed_password = pwd_context.hash(password)
    db.commit()
    return {"msg": "密码重置成功"}
