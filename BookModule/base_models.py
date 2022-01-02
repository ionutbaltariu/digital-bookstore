from typing import Dict, List
from fastapi_hypermodel import HyperModel, UrlFor, LinkSet, HALFor
from pydantic import BaseModel, constr


# find a way to share models between Modules
class IsbnStockPair(BaseModel):
    isbn: str
    quantity: int


# find a way to share models between Modules
class OrderInput(BaseModel):
    user: str
    books: List[IsbnStockPair]


class Book(HyperModel):
    isbn: str
    title: str
    publisher: str
    year_of_publishing: int
    genre: str
    price: float
    stock: int

    links = LinkSet(
        {
            "self": HALFor("get_book", {"isbn": "<isbn>"}, "Get the book"),
            "parent": HALFor("get_books", {}, "Book container"),
            "authors": HALFor("get_authors_of_book", {"isbn": "<isbn>"}, "Get the authors of the book")
        }
    )

    class Config:
        orm_mode = True


class SimplifiedBook(HyperModel):
    isbn: str
    title: str
    genre: str

    links = LinkSet(
        {
            "self": HALFor("get_book", {"isbn": "<isbn>"}, "Get the book"),
            "parent": HALFor("get_books", {}, "Book container"),
            "authors": HALFor("get_authors_of_book", {"isbn": "<isbn>"}, "Get the authors of the book")
        }
    )

    class Config:
        orm_mode = True


class Author(HyperModel):
    id: int
    first_name: str
    last_name: str

    links = LinkSet(
        {
            "self": HALFor("get_author", {"author_id": "<id>"}, "Get the author"),
        }
    )

    class Config:
        orm_mode = True


class AuthorPostBody(BaseModel):
    first_name: constr(min_length=1, max_length=64)
    last_name: constr(min_length=1, max_length=64)


class Error(BaseModel):
    error_code: int
    error_source: str
    error_reason: str


class GenericSuccess(BaseModel):
    code: int
    message: str
