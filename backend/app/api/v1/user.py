from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.database import SessionLocal
from app.schemas.user import UserLogin, UserCreate, UserOut
from app.services.user_service import UserService
from app.core.jwt_auth import create_access_token, verify_access_token
from app.models.user import User
from typing import List
from app.utils.response import fail

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")

# 权限依赖
ROLE_SUPERADMIN = 'superadmin'
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    payload = verify_access_token(token)
    if not payload:
        return fail("无效token", code=401)
    user = UserService.get_user_by_username(db, payload.get('sub'))
    if not user or not user.is_active:
        return fail("用户不存在或已禁用", code=401)
    return user

def require_roles(roles: list):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            return fail("无权限", code=403)
        return user
    return role_checker

@router.post('/login')
def login(user: UserLogin, db: Session = Depends(get_db)):
    user_obj = UserService.get_user_by_username(db, user.username)
    if not user_obj or not UserService.verify_password(user.password, user_obj.hashed_password):
        return fail("用户名或密码错误", code=400)
    if not user_obj.is_active:
        return fail("用户已禁用", code=400)
    token = create_access_token({"sub": user_obj.username, "role": user_obj.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get('/me', response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.post('/', response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    if UserService.get_user_by_username(db, user.username):
        return fail("用户名已存在", code=400)
    return UserService.create_user(db, user)

@router.get('/', response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    return db.query(User).all()

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return fail("用户不存在", code=404)
    db.delete(user)
    db.commit()
    return {"msg": "删除成功"}

@router.put('/{user_id}', response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return fail("用户不存在", code=404)
    # 超管可编辑任意用户，普通用户只能编辑自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:
        return fail("无权限", code=403)
    db_user.username = user.username
    db_user.role = user.role if current.role == ROLE_SUPERADMIN else db_user.role
    if user.password:
        from app.services.user_service import pwd_context
        db_user.hashed_password = pwd_context.hash(user.password)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post('/reset_password/{user_id}')
def reset_password(user_id: int, password: str, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return fail("用户不存在", code=404)
    # 超管可重置任意用户，普通用户只能重置自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:
        return fail("无权限", code=403)
    from app.services.user_service import pwd_context
    db_user.hashed_password = pwd_context.hash(password)
    db.commit()
    return {"msg": "密码重置成功"} 