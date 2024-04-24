# http://127.0.0.1:8000/docs #http://127.0.0.1:8000/redoc
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from app import models
# from typing import Optional
from .routers import post, user, auth, vote
from .config import settings

# you can comment this one and nothing will break
# Alembic will take good care of everything
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

routers = [
    post.router,
    user.router,
    auth.router,
    vote.router
]

origins = [
    # "http://localhost.tiangolo.com",
    # "https://localhost.tiangolo.com",
    # "http://localhost",
    # "http://localhost:8000",
    "*"  # not a good practice, remove this and specify the origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


for router in routers:
    app.include_router(router)


@app.get("/", )
def read_root():
    return "Routing success"
