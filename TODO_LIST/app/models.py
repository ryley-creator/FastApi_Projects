from sqlalchemy import String,Column,Integer,ForeignKey
from app.database import Base


class ToDo(Base):
    __tablename__ = 'todo_list'
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    title = Column(String(45),nullable=False)
    description = Column(String(100),nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,nullable=False,primary_key=True,autoincrement=True)
    name = Column(String(45),nullable=False)
    email = Column(String(45),nullable=False)
    password = Column(String(1000),nullable=False)