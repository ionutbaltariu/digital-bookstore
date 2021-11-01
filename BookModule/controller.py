from typing import List

from fastapi import FastAPI, status, Response, HTTPException
from module_constants import ErrorDto, BOOK_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, \
    CREATE_GENERIC_SUCCESS_STATUS_BODY, AUTHOR_NOT_FOUND_BODY
from model import get_book_by_isbn, delete_book_by_isbn, insert_book, update_book, get_author_by_id, \
    delete_author_by_id, insert_author, update_author, get_all_books_with_filters, get_all_authors_with_filters
import json
from utils import validate_book_post_or_put_body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi_hypermodel import HyperModel, UrlFor, LinkSet
from pydantic import BaseModel

description = """
This particular API is a module for the digital bookstore.

It allows its users to perform basic operations with book and author entities.
"""


class Book(HyperModel):
    isbn: str
    title: str
    publisher: str
    year_of_publishing: int
    genre: str

    links = LinkSet(
        {
            "self": UrlFor("get_book", {"isbn": "<isbn>"}),
            "delete_self": UrlFor("delete_book", {"isbn": "<isbn>"}),
            "put_self": UrlFor("put_book", {"isbn": "<isbn>"}),
            "books": UrlFor("get_books"),
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


app = FastAPI(
    title="Digital Bookstore - POS",
    description=description,
    version="0.0.1",
    contact={
        "name": "Ionut B.",
        "url": "https://xeno-john.github.io/"
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://github.com/xeno-john/digital-bookstore/blob/main/LICENSE",
    },
)

HyperModel.init_app(app)


@app.get("/api/bookcollection/books/", status_code=status.HTTP_200_OK, response_model=List[Book])
def get_books(response: Response, genre: str = None, year_of_publishing: int = None,
              page: int = 1, items_per_page: int = 15, ):
    """
    Method that handles a generic GET request for all of the existent books.
    """
    book_list = []
    query_parameters = {}

    if genre:
        query_parameters["genre"] = genre
    if year_of_publishing:
        query_parameters["year_of_publishing"] = year_of_publishing

    db_response = get_all_books_with_filters(**query_parameters)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        json_data = ErrorDto(status_code, str(db_response.error), 'EXCEPTION').__dict__
        raise HTTPException(status_code=500, detail=json_data)
    else:
        status_code = status.HTTP_200_OK
        for book in db_response.payload:
            book_list.append(Book.from_orm(book))
        response_body = book_list[(page - 1) * items_per_page:page * items_per_page]

    response.status_code = status_code
    return response_body


@app.get("/api/bookcollection/books/{isbn}", status_code=status.HTTP_200_OK, response_model=Book)
def get_book(isbn: str, response: Response):
    """
    Method that handles a GET request for a book by the ISBN code.
    """
    db_response = get_book_by_isbn(str(isbn))
    response_body = ''

    if db_response.error:
        json_data = ErrorDto(status.HTTP_500_INTERNAL_SERVER_ERROR, str(db_response.error), 'EXCEPTION').__dict__
        raise HTTPException(status_code=500, detail=json_data)
    elif not db_response.completed_operation:
        json_data = BOOK_NOT_FOUND_BODY.__dict__
        raise HTTPException(status_code=404, detail=json_data)
    else:
        status_code = status.HTTP_200_OK
        response_body = Book.from_orm(db_response.payload)

    response.status_code = status_code
    return response_body


@app.post("/api/bookcollection/books/", status_code=status.HTTP_201_CREATED)
def post_book(book: Book):
    print(book)
    """
    Method that handles a POST request for a book.
    """
    post_body = json.loads(book.json())
    is_valid, not_valid_reason = validate_book_post_or_put_body(post_body)
    status_code = status.HTTP_201_CREATED
    response_body = ''

    if is_valid is not True:
        status_code = status.HTTP_400_BAD_REQUEST
        response_body = ErrorDto(status_code, not_valid_reason, 'INVALID_PARAMETERS')
    else:
        db_response = insert_book(post_body)

        if db_response.error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
        else:
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.put("/api/bookcollection/books/{isbn}", status_code=status.HTTP_200_OK)
def put_book(isbn: str, book: Book):
    """
    Method that handles a PUT request for a book by the ISBN code.

    Creates the book if it doesn't already exist.
    """
    put_body = json.loads(book.json())

    is_valid, not_valid_reason = validate_book_post_or_put_body(put_body)
    status_code = status.HTTP_200_OK
    response_body = ''

    if is_valid is not True:
        status_code = status.HTTP_400_BAD_REQUEST
        response_body = ErrorDto(status_code, not_valid_reason, 'INVALID_PARAMETERS')
    elif put_body['isbn'] != isbn:
        response_body = ErrorDto(status.HTTP_406_NOT_ACCEPTABLE,
                                 'When updating a book it is not allowed to change its ISBN.',
                                 'INVALID_PARAMETERS')
    else:
        db_response = update_book(isbn, put_body)

        if db_response.error:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
        elif db_response.completed_operation is False:
            # update did not succeed because there was no book with that ISBN
            # will try POST
            db_response = insert_book(put_body)

            if db_response.error:
                status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
                response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
            else:
                status_code = status.HTTP_201_CREATED
                response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
        else:
            # update happened, status will remain 200
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.delete("/api/bookcollection/books/{isbn}", status_code=status.HTTP_200_OK)
def delete_book(isbn):
    """
    Method that handles a DELETE request for a book by the ISBN code.
    """
    db_response = delete_book_by_isbn(isbn)
    response_body = ''
    status_code = status.HTTP_200_OK
    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status_code = status.HTTP_404_NOT_FOUND
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.get("/api/bookcollection/authors/", status_code=status.HTTP_200_OK, response_model=List[Author])
def get_authors(response: Response, name: str = None):
    """
    Method that handles a generic GET request for all of the existent books.
    """
    author_list = []
    query_parameters = {}

    if name:
        query_parameters["first_name"] = name

    db_response = get_all_authors_with_filters(**query_parameters)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        json_data = ErrorDto(status_code, str(db_response.error), 'EXCEPTION').__dict__
        raise HTTPException(status_code=500, detail=json_data)
    else:
        status_code = status.HTTP_200_OK
        for author in db_response.payload:
            author_list.append(Author.from_orm(author))
        response_body = author_list

    response.status_code = status_code
    return response_body


@app.get("/api/bookcollection/authors/{author_id}", status_code=status.HTTP_200_OK, response_model=Author)
def get_author(author_id: str, response: Response):
    """
    Method that handles a GET request for an author by his id.
    """
    db_response = get_author_by_id(author_id)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        json_data = ErrorDto(status_code, str(db_response.error), 'EXCEPTION').__dict__
        raise HTTPException(status_code=500, detail=json_data)
    elif not db_response.completed_operation:
        status_code = status.HTTP_404_NOT_FOUND
        json_data = AUTHOR_NOT_FOUND_BODY.__dict__
        raise HTTPException(status_code=status_code, detail=json_data)
    else:
        status_code = status.HTTP_200_OK
        response_body = Author.from_orm(db_response.payload)

    response.status_code = status_code

    return response_body


@app.post("/api/bookcollection/authors/", status_code=status.HTTP_201_CREATED)
def post_author(author: Author):
    """
    Method that handles a POST request for an author.
    """
    post_body = json.loads(author.json())
    status_code = status.HTTP_201_CREATED
    response_body = ''

    db_response = insert_author(post_body)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    else:
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.put("/api/bookcollection/authors/{author_id}", status_code=status.HTTP_200_OK)
def put_author(author_id: str, author: Author):
    """
    Method that handles a PUT request for an author by his id.

    In this case PUT cannot behave like a POST because the id of the
    author is created in the database with an autoincrement mechanism.
    """
    put_body = json.loads(author.json())

    status_code = status.HTTP_200_OK
    response_body = ''

    db_response = update_author(author_id, put_body)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    elif db_response.completed_operation is False:
        # update did not succeed because there was no author with that id
        # will not try POST, because of the autoincrement feature of the author id
        status_code = status.HTTP_406_NOT_ACCEPTABLE
        response_body = ErrorDto(status_code,
                                 'Cannot continue with creation of the author if the author does not exist. '
                                 'Please use the POST method.',
                                 'CANNOT_COMPLETE_ACTION')

    else:
        # update happened, status will remain 200
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.delete("/api/bookcollection/authors/{author_id}", status_code=status.HTTP_200_OK)
def delete_author(author_id: str):
    """
    Method that handles a DELETE request for an author by his id.
    """
    db_response = delete_author_by_id(author_id)
    response_body = ''
    status_code = status.HTTP_200_OK
    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status_code = status.HTTP_404_NOT_FOUND
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = GENERIC_SUCCESS_STATUS_BODY

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)
