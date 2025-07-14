from pydantic import BaseModel

class CreatePost(BaseModel):
    title:str
    content:str

class CreateUser(BaseModel):
    username:str
    password:str
    section:str

class UserLogin(BaseModel):
    username:str
    password:str
class TokenData():
    id:str

class UpdatePost(BaseModel):
    title:str
    content:str
    
class CreatePostRequest(BaseModel):
    post: CreatePost