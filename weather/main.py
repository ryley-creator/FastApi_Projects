from fastapi import FastAPI,HTTPException,status
from hashlib import md5
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import redis,requests,json
from contextlib import asynccontextmanager
import uuid


base_url = 'http://api.openweathermap.org/data/2.5/weather?'
api_key = open('key.txt','r').read().strip()

@asynccontextmanager
async def lifespan(app:FastAPI):
    redis_client = redis.Redis(host='localhost',port=6379,db=0)
    app.state.redis_client = redis_client
    print('Redis client is initialized')
    yield
    redis_client.close()
    print('Redis client closed')
    
app = FastAPI(lifespan=lifespan)
    

def from_kelvin_to_celsius(kelvin):
    celsius = kelvin - 273.15
    return round(celsius,1)


@app.get('/')
def get_weather(city:str):
    redis_client = app.state.redis_client
    cache_key = city.lower()
    if redis_client.exists(cache_key):
        data = redis_client.get(cache_key)
        return json.loads(data)
    url = f'{base_url}appid={api_key}&q={city}'
    response = requests.get(url).json()
    kelvin = response['main']['temp']
    celsius = from_kelvin_to_celsius(kelvin)
    data = {'city':city,'temperature':f'{celsius}°C'}
    redis_client.setex(cache_key,600,json.dumps(data))
    return data
    
    
    
    