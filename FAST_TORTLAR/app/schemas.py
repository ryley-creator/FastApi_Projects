from pydantic import BaseModel,EmailStr
from datetime import datetime

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes = True


class TortResponse(BaseModel):
    id:int
    tort_name:str
    price:float
    posted_at:datetime
    user:UserOut
    class Config:
        from_attributes = True
class TortCreate(BaseModel):
    tort_name: str
    price: float
    posted_at: datetime
class TortUpdate(TortCreate):
    pass
class CreateUser(BaseModel):
    # id:int
    email:EmailStr
    password:str
    created_at:datetime




class TokenData(BaseModel):
    id:str