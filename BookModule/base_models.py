from fastapi_hypermodel import HyperModel, UrlFor, LinkSet
from pydantic import BaseModel, constr


class Book(HyperModel):
    isbn: str
    title: str
    publisher: str
    year_of_publishing: int
    genre: str

    links = LinkSet(
        {
            "self": UrlFor("get_book", {"isbn": "<isbn>"}),
            "authors": UrlFor("get_authors_of_book", {"isbn": "<isbn>"})
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
            "self": UrlFor("get_book", {"isbn": "<isbn>"}),
            "authors": UrlFor("get_authors_of_book", {"isbn": "<isbn>"})
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
            "self": UrlFor("get_author", {"author_id": "<id>"}),
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
