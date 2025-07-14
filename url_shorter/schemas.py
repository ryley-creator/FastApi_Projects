from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class CreateUrl(BaseModel):
    url:str

class CreateUrlResponse(BaseModel):
    id:int
    url:str
    shortCode:str
    created_at: datetime 
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class StatsResponse(BaseModel):
    id:int
    url:str
    shortCode:str
    created_at: datetime 
    updated_at: Optional[datetime]
    accessCount:int
    