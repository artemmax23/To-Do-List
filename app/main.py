from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.routers import tasks, tags

app = FastAPI(
        title="Task Manager API",
        description="API для управления задачами с тегами",
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
)

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
)

app.include_router(tasks.router)
app.include_router(tags.router)

@app.get("/", tags=["Health Check"])
async def root():
    return {
            "message": "Task Manager API is running",
            "docs": "/docs",
            "redoc": "/redoc"    
    }
    
@app.get("/health/db", tags=["Health Check"])
async def health_check():
    return {"status": "ok", "mesage": "Database is connected"}