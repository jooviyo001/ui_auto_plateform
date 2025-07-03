from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI()

app.include_router(api_router, prefix='/api/v1')

@app.get('/')
def read_root():
    return {'msg': 'UI Automation Platform API Service Running...'}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)