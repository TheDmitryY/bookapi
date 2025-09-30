from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Books(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    discription = Column(String(400))
    author = Column(String(300))

    def as_dict(self):
        return {"id": self.id, "name": self.name, "discription": self.discription, "author": self.author}