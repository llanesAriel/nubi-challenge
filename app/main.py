from fastapi import FastAPI
from routers import users
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)

app = FastAPI()
app.include_router(users.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to the Nubi Challenge API"}
