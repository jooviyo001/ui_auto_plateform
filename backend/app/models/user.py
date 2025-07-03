from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from app.models import Base

class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default='user')  # superadmin, admin, user
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)