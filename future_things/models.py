from database import Base
from sqlalchemy import Column,Integer,String

class Future(Base):
    __tablename__ = 'items'
    
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    product_name = Column(String(50),nullable=False)
    description = Column(String(500),nullable=False)
