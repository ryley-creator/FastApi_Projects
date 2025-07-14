from fastapi import APIRouter,Depends,HTTPException,status,Query
from sqlalchemy.orm import Session
import schemas,database,models,utils
from typing import List,Optional
from datetime import datetime,timedelta

router = APIRouter(
    tags=['Tracker']
)

@router.post('/create',response_model=schemas.ResponseExpense)
def create_expense(tracker:schemas.CreateExpense,db:Session=Depends(database.get_db),current_user: schemas.UserResponse = Depends(utils.get_current_user),):
    new_expense = models.Tracker(description=tracker.description,amount=tracker.amount,user_id=current_user.id)
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense

@router.get('/get',response_model=List[schemas.GetExpenses])
def get_expenses(db:Session=Depends(database.get_db),current_user:schemas.UserResponse = Depends(utils.get_current_user),
    filter: Optional[str] = Query(None),
    start_date: Optional[datetime] = Query(None),
    end_date: Optional[datetime] = Query(None)):
    query = db.query(models.Tracker).filter(models.Tracker.user_id == current_user.id)

    # Применение фильтров
    if filter == 'past_week':
        query = query.filter(models.Tracker.created_at >= datetime.now() - timedelta(weeks=1))
    elif filter == 'past_month':
        query = query.filter(models.Tracker.created_at >= datetime.now() - timedelta(days=30))
    elif filter == 'past_3_months':
        query = query.filter(models.Tracker.created_at >= datetime.now() - timedelta(days=90))
    
    if start_date and end_date:
        query = query.filter(
        models.Tracker.created_at >= start_date,
        models.Tracker.created_at <= end_date
    )
    elif start_date:
        query = query.filter(models.Tracker.created_at >= start_date)
    expenses = query.all()
    return expenses

@router.patch('/update/{id}')
def update_expense(tracker:schemas.UpdateExpense,id:int,db:Session=Depends(database.get_db),current_user:schemas.UserResponse=Depends(utils.get_current_user)):
    print('Hello world',tracker.model_dump())
    updated_data = {}
    for k,v in tracker.model_dump().items():
        if v != None:
            updated_data[k] = v
    update = db.query(models.Tracker).filter(models.Tracker.id == id,models.Users.id == current_user.id)
    updated_expense = update.first()
    
    if not updated_expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} was not found')

        
    if not current_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail={'message':'Forbidden'})
    update.update(updated_data,synchronize_session=False)
    
        
    db.commit()
    return update.first()

@router.delete('/delete/{id}')
def delete(id:int,db:Session=Depends(database.get_db),current_user:schemas.UserResponse = Depends(utils.get_current_user)):
    query = db.query(models.Tracker).filter(models.Tracker.id == id,models.Tracker.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with id {id} was not found')
    db.delete(query)
    db.commit()
    return {'msg':f'Task with id {id} was deleted succesfully!'}

@router.get('/get/{id}')
def get_by_id(id:int,db:Session=Depends(database.get_db),current_user:schemas.UserResponse = Depends(utils.get_current_user)):
    query = db.query(models.Tracker).filter(models.Tracker.id == id,models.Tracker.user_id == current_user.id).first()
    if not query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Expense with id {id} was not found')
    return query



    


    
    
    