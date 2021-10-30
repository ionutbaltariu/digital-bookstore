from fastapi import FastAPI, status
from module_constants import ErrorDto, BOOK_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, \
    CREATE_GENERIC_SUCCESS_STATUS_BODY, AUTHOR_NOT_FOUND_BODY
from model import get_book_by_isbn, delete_book_by_isbn, insert_book, update_book, get_author_by_id, \
    delete_author_by_id, insert_author, update_author, BookDto, AuthorDto
import json
from utils import validate_book_post_or_put_body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

description = """
This particular API is a module for the digital bookstore.

It allows its users to perform basic operations with book and author entities.
"""


class Book(BaseModel):
    isbn: str
    title: str
    publisher: str
    year_of_publishing: int
    genre: str


class Author(BaseModel):
    first_name: str
    last_name: str


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


@app.get("/api/bookcollection/books/{isbn}", status_code=status.HTTP_200_OK)
def get_book(isbn: str):
    """
    Method that handles a DELETE request for a book by the ISBN code.
    """
    db_response = get_book_by_isbn(str(isbn))
    response_body = ''
    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status_code = status.HTTP_404_NOT_FOUND
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = BookDto(db_response.payload)

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


@app.post("/api/bookcollection/books/", status_code=status.HTTP_201_CREATED)
def post_book(book: Book):
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


@app.get("/api/bookcollection/authors/{author_id}", status_code=status.HTTP_200_OK)
def get_author(author_id: str):
    """
    Method that handles a GET request for an author by his id.
    """
    db_response = get_author_by_id(author_id)

    if db_response.error:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        response_body = ErrorDto(status_code, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status_code = status.HTTP_404_NOT_FOUND
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = AuthorDto(db_response.payload)

    json_data = jsonable_encoder(response_body.__dict__)
    return JSONResponse(content=json_data, status_code=status_code)


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
