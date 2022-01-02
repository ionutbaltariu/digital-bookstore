from sqlalchemy.orm import relationship

from db import Base
from sqlalchemy import Column, String, Integer, Float
from json import dumps


class Book(Base):
    __tablename__ = 'books'
    isbn = Column(String(100), primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    publisher = Column(String(100), nullable=False)
    year_of_publishing = Column(Integer)
    genre = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)

    child = relationship('BooksAuthors', backref="Book", passive_deletes=True)

    def __repr__(self):
        return dumps({
            'isbn' : self.isbn,
            'title' : self.title,
            'publisher' : self.publisher,
            'year_of_publishing' : self.year_of_publishing,
            'genre' : self.genre
        })
