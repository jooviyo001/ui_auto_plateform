from sqlalchemy import Column, Integer, String, Boolean
from app.models import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    role = Column(String(20), default='user')  # superadmin, admin, user
    is_active = Column(Boolean, default=True) 