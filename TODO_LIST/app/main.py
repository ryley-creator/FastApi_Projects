from fastapi import FastAPI
from app import user,todo,database

app = FastAPI()

database.Base.metadata.create_all(bind=database.engine)

app.include_router(user.router)
app.include_router(todo.router)

@app.get("/")
async def read_root():
    return {"message": "Hello, world!"}
    

