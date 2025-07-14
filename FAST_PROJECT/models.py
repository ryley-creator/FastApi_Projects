from sqlalchemy import Integer,String,Column,Boolean,DateTime,func
from database import Base
from datetime import datetime


class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer,primary_key=True,autoincrement=True,nullable=False)
    title = Column(String(45),nullable=False)
    description = Column(String(200),nullable=False)
    completed = Column(Boolean,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())