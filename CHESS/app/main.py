from fastapi import FastAPI
from .database import engine
from . import models,auth
from .routers import user,tournaments
#used_participants = set()
# used_participants.add(participants[i].id)
# used_participants.add(participants[i].id)
# if participants[i].id in used_participants or participants[i + 1] in used_participants:
    #break

app = FastAPI()
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(tournaments.router)
models.Base.metadata.create_all(bind=engine)

@app.get('/')
def get():
    return {'message':'Hello world'}