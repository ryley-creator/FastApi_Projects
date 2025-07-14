from jose import jwt,JWTError
from datetime import datetime,timedelta
from fastapi import HTTPException,Depends,status
from . import database,schemas,models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
from .config import settings

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCES_TOKEN_EXPIRE_MINUTES = settings.acces_token_expire_minutes

def create_acces_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,ALGORITHM)
    return encoded_jwt
def verify_acces_token(token:str,credentials_exeption):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise credentials_exeption
        token_data = schemas.TokenData(id=str(user_id))
    except JWTError:
        raise credentials_exeption
    return token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    token = verify_acces_token(token,credentials_exeption)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user


