from fastapi import FastAPI
from app.routers import users
from app.database.config import init_db
from contextlib import asynccontextmanager
from os import getenv


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if getenv("ENV") != "test":
        await init_db()
        yield


app = FastAPI(lifespan=lifespan)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
