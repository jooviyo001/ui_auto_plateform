from sqlalchemy import Column, Integer, String
from app.models import Base

class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    owner = Column(String(50)) 