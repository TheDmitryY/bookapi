from fastapi import APIRouter
from books.services import add_books, get_books, del_books, update_book, get_books_by_id
from sqlalchemy import select
from database import async_session
from books.models import Books
from books.schemas import *
from typing import Optional

book_router = APIRouter(prefix="/api/v1/books")

@book_router.get("/{id}", summary="Get books by id ", tags=["📕books"])
async def gets_books_id(id: int):
    return await get_books_by_id(id=id)


@book_router.get("/",summary="Get all books", tags=["📕books"])
async def gets_books():
    return await get_books()

@book_router.post("/", tags=["📕books"], summary="Add book")
async def post_books(name: str, discription: str, author: str):
    return await add_books(name, discription, author)

@book_router.delete("/", tags=["📕books"], summary="Remove book")
async def delete_books(id: int):
    return await del_books(id)

@book_router.put("/", summary="Update info", tags=["📕books"])
async def up_books(id: int, data: Update_Books):
    return await update_book(id=id,  data=data.dict(exclude_unset=True))