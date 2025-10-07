from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import database,models,utils,oauth2
router = APIRouter(
    prefix='/login',
    tags=['Authentication']
)

@router.get('/')

def login(user_cred:OAuth2PasswordRequestForm = Depends(),db:Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.name == user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='User not found')
    if not utils.verify_password(user_cred.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='Password is incorrect')
    acces_token = oauth2.create_acces_token(data= {'user_id':user.id})
    return {'acces token':acces_token,'token type':'bearer'}

