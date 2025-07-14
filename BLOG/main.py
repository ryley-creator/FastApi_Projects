from fastapi import FastAPI,status,Request
import os,json,user,post
from datetime import datetime
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.mount('/static',StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory='templates')

jsonFile = 'posts.json'

def loadPosts():
    if os.path.exists(jsonFile) and os.path.getsize(jsonFile) > 0:
        with open(jsonFile,'r') as file:
            return json.load(file)
    return []

def savePosts(post):
    with open(jsonFile,'w') as file:
        json.dump(post,file,indent=4)
    return []

def getUniqueId(posts):
    last_id = 0
    for post in posts:
        if 'id' in post and post['id'] > last_id:
            last_id = post['id']
    return last_id
    
def current_time():
    return datetime.now().strftime("%B %d, %Y")

@app.get('/')
def hello(request:Request):
    return templates.TemplateResponse('index.html',{'request':request})

    


