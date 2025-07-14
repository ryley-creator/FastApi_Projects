from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CreateExpense(BaseModel):
    description:str
    amount:float

class ResponseExpense(BaseModel):
    id:int
    description:str
    amount:float
    created_at: datetime 
    updated_at: Optional[datetime]

class CreateUser(BaseModel):
    email:str
    password:str

class TokenData(BaseModel):
    id:str

class UserResponse(BaseModel):
    id:int
    email:str

class LoginRequest(BaseModel):
    email:str
    password:str

class UpdateExpense(BaseModel):
    description:Optional[str] = None
    amount:Optional[float] = None

class GetExpenses(BaseModel):
    id:int
    description:str
    amount:float
    created_at:datetime
    updated_at:Optional[datetime]
    # user_id:str

    class Config:
        from_attributes = True

class UpdateResponse(BaseModel):
    id:int
    description:str
    amount:float
    created_at:datetime
    updated_at:datetime




    
    