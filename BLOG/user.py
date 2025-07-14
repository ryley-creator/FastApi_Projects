import json,os,schemas,bcrypt,traceback,uuid,main
from fastapi import APIRouter,HTTPException,status,Header,Form,Depends,Request
from datetime import timedelta,datetime,timezone
from jose import jwt,JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, oauth2
from typing import Annotated

secret_key= "31e9b624e316ea2ddcb45dd48d2e5fbfcdea135affde7806dcbd48485e1982ac"
algorithm= "HS256"
acces_token_expire_minutes= 30


jsonFile = 'users.json'
router = APIRouter(
    tags=['Users']
)
bcryprt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def loadUser():
    if os.path.exists(jsonFile) and os.path.getsize(jsonFile) > 0:
        with open(jsonFile,'r') as file:
            return json.load(file)
    return []

def saveUser(user):
    with open(jsonFile,'w') as file:
        json.dump(user,file,indent=4)
       
def getUniqueId(user):
    last_id = 0
    for post in user:
        if 'id' in post and post['id'] > last_id:
            last_id = post['id']
    return last_id


def createToken(data: dict, expires_delta: timedelta = None): 
    to_encode = data.copy()
    if expires_delta: 
        expire = datetime.now() + expires_delta 
    else: 
        expire = datetime.now() + timedelta(minutes=15) 
    to_encode.update({"exp": expire}) 
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt



@router.post('/posts')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],request:Request):
    users = loadUser()
    for user in users:
        if user['username'] == form_data.username and bcryprt_context.verify(form_data.password, user['password']):
            access_token = createToken(data={'sub': user['id']})
            f = open('token.txt','w')
            f.write(access_token)
            posts = main.loadPosts()
            return main.templates.TemplateResponse("posts.html", {"request": request, "posts": posts})
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid credentials')

def verifyToken(token: Annotated[str, Depends(oauth2_scheme)]):
    print(token)
    if token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Token missing')
    try:
        payload = jwt.decode(token, secret_key,algorithms=[algorithm])
        user_id: str = payload.get('sub')
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or missing token')
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or missing token')
    return user_id



@router.get('/user/get')
def getUsers():
    users = loadUser()
    for user in users:
        userInfo = ({
            'id':user['id'],
            'username':user['username'],
            'section':user['section'],
            'password':user['password']
        })
        return userInfo
    

@router.post('/user/create')
def createUser(request:Request,username: str = Form(...), 
    password: str = Form(...), 
    section: str = Form(default="default")):
    user = loadUser()
    newId = str(uuid.uuid4())
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    newUser = {
        'id': newId,
        'username': username,
        'section': section,
        'password': hashed_password
    }
    user.append(newUser)
    saveUser(user)
    return main.templates.TemplateResponse('index.html',{'request':request})

@router.get('/user/create')
def sign_up(request:Request):
    users = loadUser()
    return main.templates.TemplateResponse('sign_up.html',{'request':request})

def getUserSection(user_id: str):
    users = loadUser()
    for user in users:
        if user['id'] == user_id:
            return user['section']
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User is not find")










        
            


