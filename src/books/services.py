from sqlalchemy import select, delete, update
from database import async_session
from books.models import Books
from books.schemas import Update_Books
from fastapi import HTTPException
from typing import Optional
import redis.asyncio as redis
import os
import json
from dotenv import load_dotenv

load_dotenv()

RedisHost = os.getenv("REDIS_HOST")
RedisPort = int(os.getenv("REDIS_PORT"))

redis_connection = redis.Redis(host=RedisHost, port=RedisPort, db=0)

async def test_redis():
    try:
        responce = redis_connection.ping()
        return {"Connection succes!"}

    except redis.ConnectionError as error:
        return {"Connection failed"}

async def get_books():
    async with async_session() as session:
        query = select(Books)
        result = await session.execute(query)
        return result.scalars().all()

async def add_books(name: str, discription: str, author: str):
    async with async_session() as session:
        new_book = Books(
            name=name,
            discription=discription,
            author=author
        )
        session.add(new_book)
        await session.commit()
        return {"status": "200", "info": "Book added"}
    
async def del_books(id: int):
    async with async_session() as session:
        result = await session.get(Books, id)
        if not result:
            # return {"status": "not found"}
            raise HTTPException(status_code=404, detail="Item not found")
        
        await session.delete(result)
        await session.commit()
        return {"status": "success"}

async def update_book(id: int, data: dict):
    async with async_session() as session:
        if not data:
            return {"status": "no changes"}

        stmt = (
            update(Books)
            .where(Books.id == id)
            .values(**data)
        )
        await session.execute(stmt)
        await session.commit()
        return {"status": "updated"}
    
async def get_books_by_id(id: int):
    key = f"book_by:{id}"
    if await redis_connection.exists(key):
        print("Take from cache")
        data = await redis_connection.get(key) 
        return json.loads(data)
    
    async with async_session() as session:
        books = await session.get(Books, id)
        if not books:
            raise HTTPException(status_code=404, detail="Item not found")
        query = select(Books).where(Books.id == id)
        result = await session.execute(query)
        book = result.scalar()

        await redis_connection.set(key, json.dumps(book.as_dict()),ex=60)
        return book