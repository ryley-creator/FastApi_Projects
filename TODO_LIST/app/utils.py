import bcrypt
from datetime import datetime,timedelta
from .import schemas,models,database
from jose import JWTError,jwt
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

def hash(password):
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password=pwd_bytes, salt=salt)
    return hashed_password.decode('utf-8')


def verify(plain_password, hashed_password):
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_byte_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password = password_byte_enc , hashed_password = hashed_password_byte_enc)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = '5dbf2a5fee3e160661725db6cf1de9b8' ()
ALGORITHM = 'HS256'
ACCES_TOKEN_EXPIRE_MINUTES = 30

def create_acces_token(data:dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    return encoded_jwt

def verify_acces_token(token: str, credentionals_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('user_id')
        if not user_id:
            raise credentionals_exception
        token_data = schemas.TokenData(id=str(user_id))
    except JWTError:
        raise credentionals_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentionals_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials'
    )
    token = verify_acces_token(token, credentionals_exception)
    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user