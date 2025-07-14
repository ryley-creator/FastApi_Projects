from pydantic import BaseModel

class Create(BaseModel):
    product_name:str
    description:str

class CreateResponse(BaseModel):
    id:int
    product_name:str
    description:str