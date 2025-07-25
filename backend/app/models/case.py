from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.models import Base

class Case(Base):
    __tablename__ = 'cases'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=False)
    group = Column(String(50))
    description = Column(Text)
    steps = Column(Text, nullable=False)  # 存储为 JSON 字符串

    project = relationship('Project') 