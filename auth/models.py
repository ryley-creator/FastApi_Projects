from database import Base
from sqlalchemy import DateTime, String,Integer,ForeignKey,Column,Float,Table

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    username = Column(String(45),unique=True,nullable=False)
    email = Column(String(100),unique=True,nullable=False)
    password = Column(String(10000),nullable=False)