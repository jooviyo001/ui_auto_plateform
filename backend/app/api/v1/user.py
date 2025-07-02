from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from app.core.database import SessionLocal
from app.schemas.user import UserLogin, UserCreate, UserOut
from app.services.user_service import UserService
from app.core.jwt_auth import create_access_token, verify_access_token
from app.models.user import User
from typing import List

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
        raise HTTPException(status_code=401, detail="无效token")
    user = UserService.get_user_by_username(db, payload.get('sub'))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="用户不存在或已禁用")
    return user

def require_roles(roles: list):
    def role_checker(user: User = Depends(get_current_user)):
        if user.role not in roles:
            raise HTTPException(status_code=403, detail="无权限")
        return user
    return role_checker

@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = UserService.get_user_by_username(db, form_data.username)
    if not user or not UserService.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户已禁用")
    token = create_access_token({"sub": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

@router.get('/me', response_model=UserOut)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.post('/', response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    if UserService.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    return UserService.create_user(db, user)

@router.get('/', response_model=List[UserOut])
def list_users(db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    return db.query(User).all()

@router.delete('/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles([ROLE_SUPERADMIN]))):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"msg": "删除成功"}

@router.put('/{user_id}', response_model=UserOut)
def update_user(user_id: int, user: UserCreate, db: Session = Depends(get_db), current: User = Depends(get_current_user)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可编辑任意用户，普通用户只能编辑自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:
        raise HTTPException(status_code=403, detail="无权限")
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
        raise HTTPException(status_code=404, detail="用户不存在")
    # 超管可重置任意用户，普通用户只能重置自己
    if current.role != ROLE_SUPERADMIN and current.id != user_id:
        raise HTTPException(status_code=403, detail="无权限")
    from app.services.user_service import pwd_context
    db_user.hashed_password = pwd_context.hash(password)
    db.commit()
    return {"msg": "密码重置成功"} 