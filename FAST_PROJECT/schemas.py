from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreateTask(BaseModel):
    title:str
    description:str
    completed:Optional[bool] = False

class ListResponse(BaseModel):
    id:int
    title:str
    description:str
    completed:bool
    created_at:datetime
    updated_at:datetime

class UpdateTask(BaseModel):
    title:str
    description:str
    completed:Optional[bool] = False
    