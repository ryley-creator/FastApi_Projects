from pydantic import BaseModel
from typing import List,Optional

class CreateToDo(BaseModel):
    title:str
    description:str

class UpdateToDo(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

class ToDoResponse(BaseModel):
    id:int
    title:str
    description:str

class CreateUser(BaseModel):
    name:str
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    name:str
    email:str

class TokenData(BaseModel):
    id:str

class LoginRequest(BaseModel):
    email:str
    password:str

class ToDoListResponse(BaseModel):
    data: List[ToDoResponse]
    page: int
    limit: int
    total: int



    