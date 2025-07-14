from  fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import utils,database,models,schemas,oauth2
from typing import List
from ..database import con
router = APIRouter(
    prefix='/users',
    tags=['Users']
)
def get_current_user_role(db: Session = Depends(database.get_db), token: str = Depends(oauth2.oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = oauth2.verify_acces_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user.role

def admin_only(role: str = Depends(get_current_user_role)):
    if role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You dont have right"
        )


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut,dependencies=[Depends(admin_only)])
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):  
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.put('/{id}',response_model=schemas.UserResponse,dependencies=[Depends(admin_only)])
def update_user_by_id(id: int, update: schemas.UpdateUser):
    conn = con.cursor(dictionary=True)
    conn.execute('select * from users where id = %s', (id,))
    bormikan_ozi = conn.fetchone()
    if not bormikan_ozi:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    conn.execute('select * from users where name = %s and id != %s', (update.name, id))
    existing_user = conn.fetchone()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this name already exists")

    conn.execute('update users set name = %s, country = %s, age = %s, rating = %s where id = %s', 
                 (update.name, update.country, update.age, update.rating, id))
    con.commit()
    conn.execute('select * from users where id = %s', (id,))
    updated_post = conn.fetchone()
    conn.close()
    return updated_post

@router.delete('/{id}',dependencies=[Depends(admin_only)])

def delete_tort(id:int,db:Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.id == id)
    first = query.first()
    if first == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='User not found')
    query.delete(synchronize_session=False)
    db.commit()
    return {'message':'succesfully deleted'}

@router.get('/',response_model=List[schemas.UserResponse])
def get_all_users(db:Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users




