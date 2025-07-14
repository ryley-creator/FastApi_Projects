from fastapi import FastAPI,Depends,HTTPException,status
from . import database,schemas,models
from sqlalchemy.orm import Session
from fastapi import Query

app = FastAPI()
models.Base.metadata.create_all(bind=database.engine)

@app.post('/post/create',response_model=schemas.PostResponse)
def create_post(post:schemas.PostCreate,db:Session = Depends(database.get_db)):
    new_post = models.Posts(
        title = post.title,content=post.content,category=post.category,tags=post.tags
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get('/posts/get')
# def get_posts(db:Session=Depends(database.get_db)):
#     posts = db.query(models.Posts).all()
#     return posts


@app.get('/posts/get')
def get_posts(term: str = Query(None), db: Session = Depends(database.get_db)):
    if term:
        posts = db.query(models.Posts).filter(
            (models.Posts.title.ilike(f"%{term}%")) | (models.Posts.content.ilike(f"%{term}%")) | (models.Posts.tags.ilike(f'%{term}%'))
        ).all()
    else:
        posts = db.query(models.Posts).all()
    return posts


@app.delete('/post/delete/{id}')
def delete_post(id:int,db:Session=Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with is {id} was not found')
    db.delete(post)
    db.commit()
    return 'Post deleted succesfully'

@app.get('/post/get/{id}')
def get_post_by_id(id:int,db:Session=Depends(database.get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} was not found')
    return post

@app.put('/post/update/{id}')
def update_post(schema:schemas.PostCreate,id:int,db:Session=Depends(database.get_db)):
    post_query = db.query(models.Posts).filter(models.Posts.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} was not found')
    post_query.update(schema.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()




    

