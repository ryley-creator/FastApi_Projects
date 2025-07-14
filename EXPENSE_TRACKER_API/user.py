from fastapi import APIRouter
import database,schemas,models,utils
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Users']
)


@router.post('/user/create', response_model=schemas.UserResponse)
def create_user(user: schemas.CreateUser, db: Session = Depends(database.get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    user_email = db.query(models.Users).filter(models.Users.email == user.email).first()
    if user_email:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This email already exists"
        )
    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post('/login')
def login(user_cred:schemas.LoginRequest,db:Session=Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_cred.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='User Not Found')
    
    if not utils.verify(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Password is incorrect')
    
    access_token = utils.create_access_token(data={'user_id': user.id})
    return {'token': access_token, 'token_type': 'bearer'}
    



    
