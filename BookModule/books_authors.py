from db import Base
from sqlalchemy import Column, String, Integer, ForeignKey


class BooksAuthors(Base):
    __tablename__ = 'books-authors'
    index = Column(Integer, nullable=False)
    isbn = Column(String(100), ForeignKey('books.isbn'), nullable=False, primary_key=True)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False, primary_key=True)
