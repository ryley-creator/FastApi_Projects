from datetime import datetime
from fastapi import FastAPI,HTTPException,status
from pydantic import BaseModel
from typing import List
app = FastAPI(
    title='Trading App'
)
users = [
    {'user_id':1,'name':'Shodiyor','lastname':'Nodirov'},
    {'user_id':2,'name':'Abdulloh','lastname':'Rakhmatullayev'},
    {'user_id':3,'name':'Kamola','lastname':'Nodirova'},
    {'user_id':4,'name':'Isfandiyor','lastname':'Nodirov','degree':{
        'id':1,'created_at':'2019-09-09','degree_type':'newbie'
    }}
]

@app.get('/users/{id}')
def get_user(id:int):
    result = []
    for user in users:
        if user.get('user_id') == id:
            result.append(user)
    return result


class Trade(BaseModel):
    id:int
    user_id:int
    currency:str
    side:str
    price:float

class Degree(BaseModel):
    id:int
    created_at: datetime
    degree_type:str


class User(BaseModel):
    id:int
    name:str
    lastname:str
    degree:List[Degree]

@app.get('/trades')
def get_trades(limit:int = 1,offset:int = 0):
    return users[:offset][:limit]


@app.post('/users/{id}')
def change_name(id:int,new_name:str):
    result = []
    for user in users:
        if user.get('id') == id:
            result.append(new_name)
    return result


trades = [
    {'id':1,'user_id':1,'currency':'BTC','side':'buy','price':123},
    {'id':2,'user_id':2,'currency':'NOT','side':'sell','price':134}
]



    

@app.post('/trades')
def add_trades(trade:List[Trade]):
    trades.extend(trade)
    return {'message':trades}



    


