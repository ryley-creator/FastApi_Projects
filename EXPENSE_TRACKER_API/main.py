from fastapi import FastAPI
import user,tracker,database
app = FastAPI()

app.include_router(user.router)
app.include_router(tracker.router)

database.Base.metadata.create_all(bind=database.engine)

