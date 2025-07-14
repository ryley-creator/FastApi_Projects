import bcrypt
from datetime import datetime,timedelta
from jose import jwt,JWTError
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import schemas,database,models
from sqlalchemy.orm import Session

def hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes,salt=salt)
    return hashed_password

def verify(plain_password,hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc,hashed_password_byte_enc)

secret_key = 'd55b9b3a01679a16cc0fece5167dca09df29befe64fb619217ad926a866c258f'
algorithm = 'HS256'
access_token_expire_minutes = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=access_token_expire_minutes)
    to_encode.update({'exp':expire})
    encoded_jwt = jwt.encode(to_encode,secret_key,algorithm=algorithm)
    return encoded_jwt

def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,secret_key,algorithms=[algorithm])
        user_id = payload.get('user_id')
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(user_id))
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentionals_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    token_data = verify_access_token(token, credentionals_exception)
    user = db.query(models.Users).filter(models.Users.id == token_data.id).first()
    if not user:
        raise credentionals_exception
    return user



