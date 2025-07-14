from sqlalchemy import String,Column,Integer,DateTime
from .database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP,DATE
from sqlalchemy.sql import func

class Posts(Base):
    __tablename__ = 'posts'

    id = Column(Integer,primary_key=True,nullable=False,autoincrement=True)
    title = Column(String(45),nullable=False)
    content = Column(String(45),nullable=False)
    category = Column(String(45),nullable=False)
    tags = Column(String(45),nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())