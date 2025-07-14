from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PostCreate(BaseModel):
    title:str
    content:str
    category:str
    tags:list

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    category: str
    tags: str
    created_at: datetime 
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True