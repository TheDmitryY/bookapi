from pydantic import BaseModel
from typing import Optional

class Books_Param(BaseModel):
    id: int
    name: str
    discription: str
    author: str

class Main_Books(BaseModel):
    name: str
    discription: str
    author: str

class New_Books(Main_Books):
    pass

class Update_Books(BaseModel):
    name: Optional[str] = None
    discription: Optional[str] = None
    author: Optional[str] = None