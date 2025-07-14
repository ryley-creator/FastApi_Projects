from fastapi import FastAPI,Depends,HTTPException,status,Response
import models,database,schemas
from sqlalchemy.orm import Session
from random_word import RandomWords

r = RandomWords()
app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.post('/shorten',response_model=schemas.CreateUrlResponse)
def create_url(url:schemas.CreateUrl,db:Session = Depends(database.get_db)):
    random_word = r.get_random_word()
    new_url = models.UrlShorter(
        url = url.url,shortCode = random_word
    )
    if not new_url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='Validation error ocurred')
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return new_url

@app.get('/get')
def get_all_urls(db:Session = Depends(database.get_db)):
    url = db.query(models.UrlShorter).all()
    return url


@app.get('/shorten/{shorten}',response_model=schemas.CreateUrlResponse)
def get_url(shorten:str,db:Session = Depends(database.get_db)):
    url_name = db.query(models.UrlShorter).filter(models.UrlShorter.shortCode == shorten).first()
    if not url_name:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Url shorten with name {shorten} was not found')
    url_name.accessCount += 1
    db.commit()
    db.refresh(url_name) 
    return url_name

@app.put('/shorten/{shorten}',response_model=schemas.CreateUrlResponse)
def update_url(schema:schemas.CreateUrl,shorten:str,db:Session = Depends(database.get_db)):
    url = db.query(models.UrlShorter).filter(models.UrlShorter.shortCode == shorten)
    updated_url = url.first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Shorten with name {shorten} was not found')
    url.update(schema.model_dump(),synchronize_session=False)
    db.commit()
    return updated_url

@app.delete('/shorten/{shorten}')
def delete_url(shorten:str,db:Session = Depends(database.get_db)):
    url = db.query(models.UrlShorter).filter(models.UrlShorter.shortCode == shorten).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Url with name {shorten} was not found')
    db.delete(url)
    db.commit()
    return {'message':f'Shorten with name {shorten} deleted succesfully!'} 

@app.get('/shorten/{shorten}/stats',response_model=schemas.StatsResponse)
def get_stats(shorten:str,db:Session = Depends(database.get_db)):
    url = db.query(models.UrlShorter).filter(models.UrlShorter.shortCode == shorten).first()
    if not url:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Shorten with name {shorten} was not found')
    return url   


    

