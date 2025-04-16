from contextlib import asynccontextmanager
from os import getenv

from fastapi import FastAPI

from app.core.database.init import init_db
from app.routers import users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if getenv("ENV") != "test":
        await init_db()
        yield


app = FastAPI(
    title="Nubi Challenge API",
    description="API para gestionar usuarios",
    version="1.0.0",
    lifespan=lifespan,
)
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "API is running"}
