from fastapi import FastAPI

app = FastAPI()

@app.post('/create')
def create_quiz():
    pass

