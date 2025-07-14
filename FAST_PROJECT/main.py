from fastapi import FastAPI,HTTPException,Depends,status
import database,models,schemas
from sqlalchemy.orm import Session


app = FastAPI()
database.Base.metadata.create_all(bind=database.engine)


@app.get('/list/{id}')
def get_list(id:int,db:Session = Depends(database.get_db)):
    get_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not get_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Task with id {id} was not found')
    return get_task

@app.post('/create')
def create(task:schemas.CreateTask,db:Session = Depends(database.get_db)):
    new_post = models.Task(
        title = task.title,description = task.description,completed = task.completed
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@app.delete('/delete')
def delete(id:int,db:Session = Depends(database.get_db)):
    get_task = db.query(models.Task).filter(models.Task.id == id).first()
    if not get_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Task with id {id} was not found')
    db.delete(get_task)
    db.commit()
    return {'message':f'Task with id {id} was deleted succesfully'}

@app.put('/update')
def update(task:schemas.UpdateTask,id:int,db:Session = Depends(database.get_db)):
    get_task = db.query(models.Task).filter(models.Task.id == id)
    updated_task = get_task.first()
    if not updated_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Task with id {id} was not found')
    get_task.update(task.model_dump(),synchronize_session=False)
    db.commit()
    return get_task.first()

@app.get('/list_tasks')
def get_tasks(db:Session = Depends(database.get_db)):
    tasks = db.query(models.Task).all()
    return tasks
    