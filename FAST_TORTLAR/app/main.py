from fastapi import FastAPI
from .routes import user,tort
from . import models,auth
from .database import engine
from .routes import user
app = FastAPI()
app.include_router(tort.router)
app.include_router(user.router)
app.include_router(auth.router)
models.Base.metadata.create_all(bind=engine)
@app.get('/')
def root():
    return {'message':'Hello world'}


