from app.models.user import User, Base
from app.schemas.user import UserCreate
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        user = UserService.get_user_by_username(db, username)
        if not user or not user.is_active:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 10):
        return db.query(User).offset(skip).limit(limit).all()