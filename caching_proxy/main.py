from fastapi import FastAPI,Request,HTTPException,status
import redis,uvicorn,json,requests,argparse
from fastapi.responses import JSONResponse


app = FastAPI()
redis_server = redis.Redis(host='localhost',port=6379,db=0,decode_responses=True)

def run_server(port:int,host:str):
    app.state.host = 'http://dummyjson.com'
    uvicorn.run(app,host='0.0.0.0',port=port)

def clear_cache():
    redis_server.flushdb()
    print('Cache succesfully cleared')

@app.get('/{path:path}')
async def proxy(path:str,request:Request):
    key = path
    cached_response = redis_server.get(key)
    
    if cached_response:
        print(f'Cache HIT {path}')
        return JSONResponse(content=json.loads(cached_response),headers={"X-Cache": "HIT"})
    host = request.app.state.host
    url = f'{host}/{path}'
    response = await requests.get(url)
    
    if response.status_code == 200:
        redis_server.setex(key,3600,json.dumps(response.json()))
        return JSONResponse(content=response.json(),headers={"X-Cache": "MISS"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Error from host server')
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Caching proxy server')
    parser.add_argument('--port',type=int,help='Enter the number of the port')
    parser.add_argument('--host',type=str,help='Enter the host that you want to work with')
    parser.add_argument('--clear-cache',help='Enter it to clear the cache')
    
    args = parser.parse_args()
    
    if args.port and args.host:
        run_server(args.port,args.host)
    elif args.clear_cache:
        clear_cache()
    else:
        print("Please provide both --port and --origin arguments to start the proxy server.")
    
        
        
    
    
















