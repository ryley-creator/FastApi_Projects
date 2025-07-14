from sqlalchemy import String,Column,Integer,Float,DateTime,func,ForeignKey
from database import Base


class Tracker(Base):
    __tablename__ = 'tracker'
    id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    description = Column(String(100),nullable=False)
    amount = Column(Float,nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
   
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    email = Column(String(45),nullable=False)
    password = Column(String(1000),nullable=False)