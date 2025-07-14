from sqlalchemy.orm import relationship
from sqlalchemy import String,Integer,ForeignKey,Column,Float
from .database import Base
from sqlalchemy.sql.sqltypes import DATE,TIMESTAMP

class Tortlar(Base):
    __tablename__ = 'tortlar'

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    tort_name = Column(String(45),nullable=False)
    price = Column(Float,nullable=False)
    posted_at = Column(DATE,nullable=False,default='2019-09-09')
    user_id = Column(Integer,ForeignKey('users.id',ondelete='CASCADE'),nullable=False)
    user = relationship("Users", back_populates="torts")
    
    

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    email = Column(String(45),nullable=False,unique=True)
    password = Column(String(10000),nullable = False)
    created_at = Column(DATE,nullable=False,default='2019-09-09')
    torts = relationship("Tortlar", back_populates="user")
