from fastapi import FastAPI
from .routers import chats

from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)

app.include_router(chats.router)

app.mount('/testchat', StaticFiles(directory="app/test", html=True), name='testchat')

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}