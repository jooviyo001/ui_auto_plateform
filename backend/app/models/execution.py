from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime

Base = declarative_base()

class ExecutionTask(Base):
    __tablename__ = 'execution_tasks'
    id = Column(Integer, primary_key=True, index=True)
    celery_task_id = Column(String(100), unique=True, nullable=False)
    status = Column(String(20), default='PENDING')  # PENDING, STARTED, SUCCESS, FAILURE
    case_ids = Column(Text)  # 存储用例ID列表，JSON字符串
    result = Column(Text)    # 批量结果，JSON字符串
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)

class ExecutionResult(Base):
    __tablename__ = 'execution_results'
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey('execution_tasks.id'))
    case_id = Column(Integer)
    success = Column(Integer)  # 1=成功, 0=失败
    steps_result = Column(Text)
    error = Column(Text)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime)

    task = relationship('ExecutionTask') 