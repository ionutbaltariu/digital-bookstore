from typing import List

import uvicorn
from fastapi import FastAPI, status, Response, HTTPException
from module_constants import BOOK_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, \
    CREATE_GENERIC_SUCCESS_STATUS_BODY, AUTHOR_NOT_FOUND_BODY, get_error_body
from model import get_book_by_isbn, delete_book_by_isbn, insert_book, update_book, get_author_by_id, \
    delete_author_by_id, insert_author, update_author, get_all_books_with_filters, get_all_authors_with_filters, \
    get_all_authors_of_book, add_author_to_book, delete_author_from_book
import json
from utils import validate_book_post_or_put_body
from fastapi.responses import JSONResponse
from fastapi_hypermodel import HyperModel
from base_models import Book, SimplifiedBook, Author, AuthorPostBody, Error, GenericSuccess, OrderInput
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

def get_documentation_for_specific_resource(endpoint: str) -> dict:
    openapi_schema = get_openapi(
        title="OpenAPI Documentation",
        version="0.0.01",
        description="This is the schema of the API.",
        routes=app.routes,
    )
    if endpoint == "whole_api":
        return openapi_schema["paths"]
    else:
        return openapi_schema["paths"][endpoint]


description = """
This particular API is a module for the digital bookstore.

It allows its users to perform basic operations with book and author entities.
"""

tags_metadata = [
    {
        "name": "Books",
        "description": "Operations with books.",
    },
    {
        "name": "Authors",
        "description": "Operations with authors.",
    },
    {
        "name": "Authors of a book",
        "description": "Operations with the authors of a specific book."
    },
    {
        "name": "Specific documentation links",
        "description": "Can be used to check the structure of the API for various endpoints."
    }
]

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

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HyperModel.init_app(app)


@app.get("/api/bookcollection/books/",
         responses={200: {"model": List[Book]},
                    500: {"model": Error}},
         response_model=List[Book],
         tags=["Books"])
def get_books(genre: str = None, year_of_publishing: int = None,
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
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        for book in db_response.payload:
            book_list.append(Book.from_orm(book).dict())
        response_body = book_list[(page - 1) * items_per_page:page * items_per_page]

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/api/bookcollection/books/{isbn}",
         responses={200: {"model": Book},
                    404: {"model": Error},
                    500: {"model": Error}},
         response_model=Book,
         tags=["Books"]
         )
def get_book(isbn: str, verbose: bool = True):
    """
    Method that handles a GET request for a book by the ISBN code.
    """
    db_response = get_book_by_isbn(str(isbn))

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = 200

        if verbose:
            response_body = Book.from_orm(db_response.payload).dict()
        else:
            response_body = SimplifiedBook.from_orm(db_response.payload).dict()

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/api/bookcollection/books/",
          responses={201: {"model": GenericSuccess},
                     406: {"model": Error},
                     500: {"model": Error}},
          response_model=GenericSuccess,
          tags=["Books"]
          )
def post_book(book: Book):
    """
    Method that handles a POST request for a book.
    """
    post_body = json.loads(book.json())
    is_valid, not_valid_reason = validate_book_post_or_put_body(post_body)

    if is_valid is not True:
        status_code = 406
        response_body = get_error_body(status_code, not_valid_reason, "INVALID_PARAMETERS")
    else:
        db_response = insert_book(post_body)

        if db_response.error:
            status_code = 500
            response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
        else:
            status_code = 201
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.put("/api/bookcollection/books/{isbn}",
         responses={200: {"model": GenericSuccess},
                    500: {"model": Error},
                    406: {"model": Error}},
         response_model=GenericSuccess,
         tags=["Books"]
         )
def put_book(isbn: str, book: Book):
    """
    Method that handles a PUT request for a book by the ISBN code.

    Creates the book if it doesn't already exist.
    """
    put_body = json.loads(book.json())

    is_valid, not_valid_reason = validate_book_post_or_put_body(put_body)

    if is_valid is not True:
        status_code = 406
        response_body = get_error_body(status_code, not_valid_reason, "INVALID_PARAMETERS")
    elif put_body['isbn'] != isbn:
        status_code = 406
        response_body = get_error_body(status_code,
                                       "When updating a book it is not allowed to change its ISBN.",
                                       "INVALID_PARAMETERS")

    else:
        db_response = update_book(isbn, put_body)

        if db_response.error:
            status_code = 500
            response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
        elif db_response.completed_operation is False:
            # update did not succeed because there was no book with that ISBN
            # will try POST
            db_response = insert_book(put_body)

            if db_response.error:
                status_code = 500
                response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
            else:
                status_code = 201
                response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
        else:
            # update happened, status will remain 200
            status_code = 200
            response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.delete("/api/bookcollection/books/{isbn}",
            response_model=GenericSuccess,
            responses={500: {"model": Error},
                       404: {"model": Error},
                       200: {"model": GenericSuccess}},
            tags=["Books"])
def delete_book(isbn):
    """
    Method that handles a DELETE request for a book by the ISBN code.
    """
    db_response = delete_book_by_isbn(isbn)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = BOOK_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/api/bookcollection/authors/",
         response_model=List[Author],
         responses={200: {"model": List[Author]},
                    500: {"model": Error}},
         tags=["Authors"])
def get_authors(name: str = None):
    """
    Method that handles a generic GET request for all of the existent books.
    """
    author_list = []
    query_parameters = {}

    if name:
        query_parameters["first_name"] = name

    db_response = get_all_authors_with_filters(**query_parameters)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        for author in db_response.payload:
            author_list.append(Author.from_orm(author))
        response_body = author_list

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/api/bookcollection/authors/{author_id}",
         response_model=Author,
         responses={200: {"model": GenericSuccess},
                    500: {"model": Error},
                    404: {"model": Error}},
         tags=["Authors"])
def get_author(author_id: str):
    """
    Method that handles a GET request for an author by his id.
    """
    db_response = get_author_by_id(author_id)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = status.HTTP_200_OK
        response_body = Author.from_orm(db_response.payload).dict()

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/api/bookcollection/authors/",
          response_model=GenericSuccess,
          responses={201: {"model": GenericSuccess},
                     500: {"model": Error}},
          tags=["Authors"])
def post_author(author: AuthorPostBody):
    """
    Method that handles a POST request for an author.
    """
    post_body = json.loads(author.json())

    db_response = insert_author(post_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        status_code = 200
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.put("/api/bookcollection/authors/{author_id}",
         response_model=GenericSuccess,
         responses={200: {"model": GenericSuccess},
                    500: {"model": Error},
                    406: {"model": Error}},
         tags=["Authors"])
def put_author(author_id: str, author: AuthorPostBody):
    """
    Method that handles a PUT request for an author by his id.

    In this case PUT cannot behave like a POST because the id of the
    author is created in the database with an autoincrement mechanism.
    """
    put_body = json.loads(author.json())
    db_response = update_author(author_id, put_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif db_response.completed_operation is False:
        # update did not succeed because there was no author with that id
        # will not try POST, because of the autoincrement feature of the author id
        status_code = 406
        response_body = get_error_body(status_code,
                                       'Cannot continue with creation of the author if the author does not exist. '
                                       'Please use the POST method.',
                                       "EXCEPTION")
    else:
        # update happened, status will remain 200
        status_code = 200
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.delete("/api/bookcollection/authors/{author_id}",
            response_model=GenericSuccess,
            responses={200: {"model": GenericSuccess},
                       500: {"model": Error},
                       404: {"model": Error}},
            tags=["Authors"])
def delete_author(author_id: str):
    """
    Method that handles a DELETE request for an author by his id.
    """
    db_response = delete_author_by_id(author_id)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 404
        response_body = AUTHOR_NOT_FOUND_BODY
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.get("/api/bookcollection/books/{isbn}/authors",
         response_model=List[Author],
         responses={500: {"model": Error},
                    200: {"model": List[Author]}},
         tags=["Authors of a book"])
def get_authors_of_book(isbn: str, response: Response):
    """
    Method that handles a GET request for the authors of a book by the book's ISBN.
    """
    db_response = get_all_authors_of_book(isbn)
    response_body = []

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    else:
        for author in db_response.payload:
            response_body.append(Author.from_orm(author).dict())
        status_code = 200

    return JSONResponse(status_code=status_code, content=response_body)


@app.post("/api/bookcollection/books/{isbn}/authors",
          response_model=GenericSuccess,
          responses={201: {"model": GenericSuccess},
                     500: {"model": Error},
                     406: {"model": Error}},
          tags=["Authors of a book"])
def add_author_to_book_by_isbn(isbn: str, author: AuthorPostBody):
    """
    Can be used to add an author to a specific book (identified by ISBN)
    """
    post_body = json.loads(author.json())
    db_response = add_author_to_book(isbn, post_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif not db_response.completed_operation:
        status_code = 406
        response_body = get_error_body(status_code,
                                       'Could not insert author / Author is already related to the book',
                                       "ALREADY_EXISTENT_RESOURCE")
    else:
        status_code = 201
        response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.delete("/api/bookcollection/books/{isbn}/authors",
            response_model=GenericSuccess,
            responses={500: {"model": Error},
                       404: {"model": Error},
                       200: {"model": GenericSuccess}},
            tags=["Authors of a book"])
def delete_author_from_book_by_isbn(isbn: str, author: AuthorPostBody):
    """
    Can be used to delete an author from a specific book (identified by ISBN)
    """
    post_body = json.loads(author.json())
    print(post_body)
    db_response = delete_author_from_book(isbn, post_body)

    if db_response.error:
        status_code = 500
        response_body = get_error_body(status_code, str(db_response.error), "EXCEPTION")
    elif db_response.client_error:
        status_code = 404
        response_body = get_error_body(status_code, str(db_response.client_error), 'NONEXISTENT_RESOURCE')
    else:
        status_code = 200
        response_body = GENERIC_SUCCESS_STATUS_BODY

    return JSONResponse(status_code=status_code, content=response_body)


@app.options("/api/bookcollection/",
             status_code=status.HTTP_200_OK,
             tags=["Specific documentation links"])
def get_documentation_for_api():
    """
    Make a HTTP OPTIONS call to this endpoint to get the documentation for the whole API.
    """
    return get_documentation_for_specific_resource("whole_api")


@app.options("/api/bookcollection/books",
             status_code=status.HTTP_200_OK,
             tags=["Specific documentation links"])
def get_documentation_for_books():
    """
    Make a HTTP OPTIONS call to this endpoint to get the documentation for /books branch of endpoints.
    """
    return get_documentation_for_specific_resource("/api/bookcollection/books/{isbn}")


@app.options("/api/bookcollection/authors",
             status_code=status.HTTP_200_OK,
             tags=["Specific documentation links"])
def get_documentation_for_books():
    """
    Make a HTTP OPTIONS call to this endpoint to get the documentation for /authors branch of endpoints.
    """
    return get_documentation_for_specific_resource("/api/bookcollection/authors/{author_id}")


@app.post("/api/bookcollection/process-order-and-adapt-stocks",
         response_model=List[Book],
         responses={500: {"model": Error},
                    404: {"model": Error},
                    409: {"model": Error},
                    200: {"model": List[Book]}},
         tags=["Orders"])
def process_order(order_input: OrderInput):
    """
    Method that a POST request that is meant to be an intermediate for the orders module.

    The method receives a list of ISBN's paired with a quantity and checks whether the
    given books are available to be placed in an order or not.
    """
    db_response = get_all_books_with_filters()
    all_books_indexed = {}
    updated_books = []
    # we make a dict with key as the book's ISBN
    # and as value, the book itself
    # this way we avoid making a SELECT for every book
    # in the order
    response_body = None
    status_code = 200

    if db_response.payload:
        all_books = db_response.payload

        for book in all_books:
            all_books_indexed[Book.from_orm(book).dict()["isbn"]] = Book.from_orm(book).dict()

        response_body = []

        for ordered_book in order_input.books:
            isbn = ordered_book.dict()['isbn']
            if isbn in all_books_indexed:
                actual_stock = all_books_indexed[isbn]['stock']
                if actual_stock - ordered_book.quantity >= 0:
                    current_book = all_books_indexed[isbn]
                    current_book["stock"] -= ordered_book.quantity
                    response_body.append(current_book)
                    updated_books.append(current_book)
                else:
                    updated_books = []
                    status_code = 409
                    response_body = get_error_body(409,
                                                   f"Cannot proceed with the command,"
                                                   f" there are not enough books with the isbn '{isbn}'",
                                                   f"Required: {ordered_book.quantity}, available: {actual_stock}")
                    break

            else:
                status_code = 404
                response_body = get_error_body(404, f"Book with the isbn: '{isbn}' does not exist.", "ERROR")
                break
    else:
        status_code = 500
        response_body = get_error_body(500, str(db_response.error), "EXCEPTION")

    for updated_book in updated_books:
        update_book(updated_book['isbn'], {'stock': updated_book['stock']})

    return JSONResponse(status_code=status_code, content=response_body)


if __name__ == "__main__":
    uvicorn.run("controller:app", host='0.0.0.0', port=8000, reload=True, debug=True)
