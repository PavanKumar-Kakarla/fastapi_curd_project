from fastapi import FastAPI
from app.routes import items, clock_in


app = FastAPI()

app.include_router(items.router)
app.include_router(clock_in.router)


@app.get('/')
async def welcome():
    return {"message": "Hello welcome to FastAPI."} 