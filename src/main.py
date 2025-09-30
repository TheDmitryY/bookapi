from fastapi import FastAPI, APIRouter
from books.router import book_router
from admins.router import admin_router
from database import init_db

app = FastAPI(title="BookAPI", version="0.0.1", docs_url="/api/v1/docs")
router = APIRouter(prefix="/api/v1")

@router.get("/")
async def welcome():
    return {"message": "Hello"}

app.include_router(router)
app.include_router(book_router)
app.include_router(admin_router)

@app.on_event("startup")
async def startup_event():
    await init_db()

@app.on_event("shutdown")
async def shutdown_event():
    print("App stoped!")