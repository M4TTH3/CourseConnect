from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from .routers import chats, users, posts
from .internal.auth import auth, AuthUser

from fastapi.staticfiles import StaticFiles

app = FastAPI()

origins = [
    "http://localhost:5000",
    "courseconnect:///"
    
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chats.router)
app.include_router(users.router)
app.include_router(posts.router)

app.mount('/testchat', StaticFiles(directory="app/test", html=True), name='testchat')

@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}


@app.get("/tokentest")
async def tokentest(auth_result: AuthUser = Security(auth.verify, scopes=['read:profile'])):
    return str(auth_result)

