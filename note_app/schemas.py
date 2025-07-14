from pydantic import BaseModel

class FileListResponse(BaseModel):
    id:int
    filename:str
    note:str
    
    class Config:
        from_attributes = True 
