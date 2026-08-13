from fastapi import FastAPI
from app.database import engine

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Привет!"}