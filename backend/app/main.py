from fastapi import FastAPI
from .database import engine, Base
from . import models

app = FastAPI()

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "SHACC Backend is running!"}