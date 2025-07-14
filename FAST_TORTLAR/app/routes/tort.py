from fastapi import APIRouter,HTTPException,status
from ..database import con,get_db
from .. import schemas
from typing import List
from pydantic import TypeAdapter
import mysql.connector
from sqlalchemy.orm import Session
from fastapi import Depends
from .. import models,oauth2

router = APIRouter(
    prefix='/tort',
    tags=['tortlar']
)

@router.get('/')
def get_tort(db: Session = Depends(get_db)):
    torts = db.query(models.Tortlar).all()
    return torts

@router.post('/')
def create_tort_post(tort:schemas.TortCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    new_tort = models.Tortlar(
        tort_name = tort.tort_name,price = tort.price,posted_at = tort.posted_at,user_id = current_user.id
    )
    db.add(new_tort)
    db.commit()
    db.refresh(new_tort)
    return new_tort
    

@router.get('/{id}')

def get_tort_id(id:int):
    conn = con.cursor(dictionary=True)
    conn.execute('select * from tortlar where id = %s',(id,))
    tort = conn.fetchone()
    return tort

@router.delete('/{id}')

def delete_tort(id:int,db:Session = Depends(get_db)):
    query = db.query(models.Tortlar).filter(models.Tortlar.id == id)
    first = query.first()
    if first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='tort not found')
    query.delete(synchronize_session=False)
    db.commit()
    return {'message':'succesfully deleted'}

@router.put('/{id}')

def update_tort_post(id:int,update:schemas.TortUpdate):
    conn = con.cursor(dictionary=True)
    conn.execute('select * from tortlar where id = %s',(id,))
    bormikan_ozi = conn.fetchone()
    if not bormikan_ozi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    conn.execute('update tortlar set tort_name = %s,price = %s,posted_at = %s where id = %s',(update.tort_name,update.price,update.posted_at,id,))
    con.commit()
    conn.execute('select * from tortlar where id = %s',(id,))
    updated_post = conn.fetchone()
    return updated_post

    
    

    


