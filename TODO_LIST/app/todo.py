from fastapi import APIRouter,Depends,HTTPException,status,Query
from app import schemas,database,models,utils
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter(
    tags=['ToDo']
)

@router.post('/create',response_model=schemas.ToDoResponse)
def create(todo:schemas.CreateToDo,db:Session=Depends(database.get_db),current_user: schemas.UserResponse = Depends(utils.get_current_user)):
    new_todo = models.ToDo(
        title = todo.title,description = todo.description,user_id=current_user.id
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


    
# @router.get('/get')
# def get(db:Session=Depends(database.get_db),current_user: schemas.UserResponse = Depends(utils.get_current_user)):
#     todo = db.query(models.ToDo).all()
#     return todo

@router.get('/get')
def get(
    title:Optional[str] = Query(None,description='Title'),
    page: int = 1, 
    limit: int = 10,
    db: Session = Depends(database.get_db), 
    current_user: schemas.UserResponse = Depends(utils.get_current_user)
):
    if page < 1 or limit < 1:
        raise HTTPException(status_code=400, detail="Page and limit must be greater than 0")
    
    query = db.query(models.ToDo).filter(models.ToDo.user_id == current_user.id)
    if title:
        query = query.filter(models.ToDo.title.ilike(f"%{title}%"))
    
    skip = (page - 1) * limit
    
    # todos = db.query(models.ToDo).offset(skip).limit(limit).all()
    todos = query.offset(skip).limit(limit).all()
    total = query.count()

    return {
        "data": todos,
        "page": page,
        "limit": limit,
        "total": total
    }

@router.get('/get/{id}')
def get_id(id:int,db:Session=Depends(database.get_db),current_user: schemas.UserResponse = Depends(utils.get_current_user)):
    query = db.query(models.ToDo).filter(models.ToDo.id == id,models.ToDo.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ToDo with id {id} was not found')
    return query

@router.put('/update/{id}',response_model=schemas.UpdateResponse)
def update(todo:schemas.UpdateToDo,id:int,db:Session=Depends(database.get_db),current_user: schemas.UserResponse = Depends(utils.get_current_user)):
    update = db.query(models.ToDo).filter(models.ToDo.id == id,models.ToDo.user_id == current_user.id)
    updated_todo = update.first()
    if not updated_todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ToDo with id {id} was not found') 
    if todo.title is not None:
        updated_todo.title = todo.title
    if todo.description is not None:
        updated_todo.description = todo.description
    # update.update(todo.model_dump(),synchronize_session=False)
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'message':'Forbidden'})
    db.commit()
    return update.first()

@router.delete('/delete/{id}',status_code=204)
def delete(id:int,db:Session=Depends(database.get_db),current_user:schemas.UserResponse = Depends(utils.get_current_user)):
    query = db.query(models.ToDo).filter(models.ToDo.id == id,models.ToDo.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'ToDo with id {id} was not found')
    db.delete(query)
    db.commit()
    return {'meassge':'ToDo deleted succesfully'}





 









    
    