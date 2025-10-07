from fastapi import FastAPI
import user,models,database,auth

app = FastAPI()

app.include_router(user.router)
app.include_router(auth.router)
models.Base.metadata.create_all(bind=database.engine)