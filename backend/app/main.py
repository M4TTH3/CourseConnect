from fastapi import FastAPI, Security
from .routers import chats
from .internal.auth import VerifyJWT

from fastapi.staticfiles import StaticFiles

app = FastAPI(debug=True)
auth = VerifyJWT()

app.include_router(chats.router)

app.mount('/testchat', StaticFiles(directory="app/test", html=True), name='testchat')

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/tokentest")
async def tokentest(auth_result: str = Security(auth.verify, scopes=['read:profile'])):
    return auth_result