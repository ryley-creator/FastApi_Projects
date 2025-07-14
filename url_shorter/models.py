from sqlalchemy import Column,Integer,String,DateTime
from database import Base
from sqlalchemy.sql import func

class UrlShorter(Base):
    __tablename__ = 'urls'
    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    url = Column(String(50),nullable=False)
    shortCode = Column(String(20),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    accessCount = Column(Integer,nullable=True,default=0)