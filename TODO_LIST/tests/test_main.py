from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
import pytest
from app.models import Users,ToDo  # SQLAlchemy-модель
from app import utils
import time

client = TestClient(app)
database_url = 'mysql+pymysql://root:12341234@127.0.0.1:3306/test_db'


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base

# Тестовый движок MySQL
test_engine = create_engine(database_url)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Создаем таблицы в тестовой базе
Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    # Перед каждым тестом очищаем базу
    Base.metadata.drop_all(bind=test_engine)
    print('hello man')
    Base.metadata.create_all(bind=test_engine)


# def test_user_create(test_db):
#     response = client.post('/user/create',json={'name':'shodiyor','email':'sh@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     assert response.json()['name'] == 'shodiyor'
    
#     db = TestingSessionLocal()
#     user = db.query(Users).filter(Users.email == 'sh@gmail.com').first()
#     print(user)
#     assert user is not None
#     assert user.name == 'shodiyor'

# def test_login():
#     hashed_password = utils.hash('12341234')
    
#     db = TestingSessionLocal()
#     new_user = Users(name='abdullah',email='abdullah@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     response = client.post('/login',json={'email':'abdullah@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     assert 'token' in response.json()
    

# def test_password():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='/cabdullah',email='abdullah1997@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     respone = client.post('/login',json={'email':'abdullah1997@gmail.com','password':'123412345'})
#     assert respone.status_code == 403
#     assert respone.json() == {'detail':'Password is incorrect'}
    
# def test_email():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='shodiyor',email='shodiyor2008@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    

# def test_check_auth_create_todo():
#     response = client.post('/create',json={'title':'hello world','description':'hi my name is shodiyor'})
#     assert response.status_code == 401
#     assert response.json() == {'detail':'Not authenticated'}

# def test_get_not_authorized():
#     response = client.get('/get')
#     assert response.status_code == 401
#     assert response.json() == {'detail':'Not authenticated'}

# def test_get_todo_authorized():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='banana',email='banana@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     new_todo = ToDo(title='Hello world',description='My name is shodiyor',user_id=new_user.id)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
    
#     response = client.post('/login',json={'email':'banana@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     access_token = response.json()['token']
    
#     headers = {'Authorization':f'Bearer {access_token}'}
#     response = client.get('/get',headers=headers)
#     assert response.status_code == 200
#     assert response.json()['data'][0]['id'] == new_todo.id

# def test_get_by_id():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='messi',email='messi@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     new_todo = ToDo(title='Hello world',description='My name is shodiyor',user_id=new_user.id)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
    
#     response = client.post('/login',json={'email':'messi@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     access_token = response.json()['token']
    
#     headers = {'Authorization':f'Bearer {access_token}'}
#     response = client.get(f'/get/{new_todo.id}',headers=headers)
#     assert response.status_code == 200
    


# def test_create_not_authorized():
#     response = client.post("/create")
#     assert response.status_code == 401
#     assert response.json() == {"detail": "Not authenticated"}

# def test_create_authorized():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='nodir',email='nodir@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     response = client.post('/login',json={'email':'nodir@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     access_token = response.json()['token']
    
#     headers = {'Authorization': f'Bearer {access_token}'}
#     response = client.post('/create',json={'title':'hello world','description':'hi my name is shodiyor'},headers=headers)
#     assert response.status_code == 200
#     assert response.json()['title'] == 'hello world'
#     assert response.json()['description'] == 'hi my name is shodiyor'
    

# def test_update_not_found_error():
#     response = client.put('/update',json={'title':'Hello world','description':'My name is shodiyor'})
#     response.status_code == 404
#     assert response.json() == {'detail':'Not Found'}


# def test_update_todo():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='kamola',email='kamola@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     new_todo = ToDo(title='Hello world',description='My name is shodiyor',user_id=new_user.id)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
    
#     response = client.post('/login',json={'email':'kamola@gmail.com','password':'12341234'})
#     assert response.status_code == 200
#     access_token = response.json()['token']
    
#     headers = {'Authorization':f'Bearer {access_token}'}
#     response = client.put(f'/update/{new_todo.id}',json={'title':'I am dangerous','description':'my name is janet'},headers=headers)
#     assert response.status_code == 200
#     assert response.json()['title'] == 'I am dangerous'
#     assert response.json()['description'] == 'my name is janet'

def test_delete_todo(test_db):
    hashed_password = utils.hash('12341234')
    db = TestingSessionLocal()
    new_user = Users(name='lemonjon',email='lemonjon@gmail.com',password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    new_todo = ToDo(title='gg',description='wp',user_id=new_user.id)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    
    response = client.post('/login',json={'email':'lemonjon@gmail.com','password':'12341234'})
    assert response.status_code == 200
    access_token = response.json()['token']

    headers ={'Authorization':f'Bearer {access_token}'}
    response = client.delete(f'/delete/{new_todo.id}',headers=headers)
    assert response.status_code == 204
    db.close()
    assert db.query(ToDo).first() == None


# def test_delete_unauthorized():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='diyor',email='diyor@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     new_todo = ToDo(title='Hello world',description='My name is shodiyor',user_id=new_user.id)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
    
#     response = client.post('/login',json={'email':'diyor@gmail.com','password':'12341234'})
#     assert response.status_code == 200
    
#     response = client.delete(f'/delete/{new_todo.id}')
#     assert response.status_code == 401

# def test_update_unauthorized():
#     hashed_password = utils.hash('12341234')
#     db = TestingSessionLocal()
#     new_user = Users(name='bobur',email='bobur@gmail.com',password=hashed_password)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
    
#     new_todo = ToDo(title='Hello world',description='My name is shodiyor',user_id=new_user.id)
#     db.add(new_todo)
#     db.commit()
#     db.refresh(new_todo)
    
#     response = client.post('/login',json={'email':'bobur@gmail.com','password':'12341234'})
#     assert response.status_code == 200
    
#     response = client.put(f'/update/{new_todo.id}',json={'title':'Hello','description':'gg bro'})
#     assert response.status_code == 401
    
    
    
    
    
    



    






    







    
    


