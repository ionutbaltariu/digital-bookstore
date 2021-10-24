from module_constants import ErrorDto, StatusDto, BOOK_NOT_FOUND_BODY, GENERIC_SUCCESS_STATUS_BODY, \
    CREATE_GENERIC_SUCCESS_STATUS_BODY, AUTHOR_NOT_FOUND_BODY
from flask import Flask, jsonify, request
from model import get_book_by_isbn, delete_book_by_isbn, insert_book, update_book, get_author_by_id, \
    delete_author_by_id, insert_author, update_author
import json
from utils import validate_book_post_or_put_body, validate_author_post_or_put_body

app = Flask(__name__)


class BookDto:
    def __init__(self, book, links):
        self.isbn = book.isbn
        self.title = book.title
        self.publisher = book.publisher
        self.year_of_publishing = book.year_of_publishing
        self.genre = book.genre
        self.links = links.__dict__


class LinkDto:
    def __init__(self, href, rel, method_type):
        self.href = href
        self.rel = rel
        self.type = method_type


class AuthorDto:
    def __init__(self, author, links):
        self.first_name = author.first_name
        self.last_name = author.last_name
        self.links = links.__dict__


@app.route('/api/bookcollection/books/<isbn>', methods=['GET'])
def get_book(isbn):
    """
    Method that handles a GET request for a book by the ISBN code.

    :param isbn: isbn code of the book that is to be retrieved
    """
    db_response = get_book_by_isbn(str(isbn))
    body = ''
    status = 200
    if db_response.error:
        status = 500
        body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status = 404
        body = BOOK_NOT_FOUND_BODY
    else:
        status = 200
        links = LinkDto(request.path, 'books', request.method)
        body = BookDto(db_response.payload, links)

    return jsonify(body.__dict__), status


@app.route('/api/bookcollection/books/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    """
    Method that handles a DELETE request for a book by the ISBN code.

    :param isbn: isbn code of the book that is to be deleted
    """
    db_response = delete_book_by_isbn(isbn)
    body = ''
    status = 200
    if db_response.error:
        status = 500
        body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status = 404
        body = BOOK_NOT_FOUND_BODY
    else:
        status = 200
        links = LinkDto(request.path, 'books', request.method)
        body = GENERIC_SUCCESS_STATUS_BODY
        body.set_links(links)

    return jsonify(body.__dict__), status


@app.route('/api/bookcollection/books/', methods=['POST'])
def post_book():
    post_body = json.loads(request.get_data())
    is_valid, not_valid_reason = validate_book_post_or_put_body(post_body)
    status = 201
    response_body = ''

    if is_valid is not True:
        status = 400
        response_body = ErrorDto(400, not_valid_reason, 'INVALID_PARAMETERS')
    else:
        db_response = insert_book(post_body)

        if db_response.error:
            status = 500
            response_body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
        else:
            links = LinkDto(request.path + post_body['isbn'], 'books', request.method)
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
            response_body.set_links(links)

    return jsonify(response_body.__dict__), status


@app.route('/api/bookcollection/books/<isbn>', methods=['PUT'])
def patch_book(isbn):
    put_body = json.loads(request.get_data())

    is_valid, not_valid_reason = validate_book_post_or_put_body(put_body)
    status = 200
    response_body = ''

    if is_valid is not True:
        status = 400
        response_body = ErrorDto(400, not_valid_reason, 'INVALID_PARAMETERS')
    elif put_body['isbn'] != isbn:
        response_body = ErrorDto(400,
                                 'When updating a book it is not allowed to change its ISBN.',
                                 'INVALID_PARAMETERS')
    else:
        db_response = update_book(isbn, put_body)

        if db_response.error:
            status = 500
            response_body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
        elif db_response.completed_operation is False:
            # update did not succeed because there was no book with that ISBN
            # will try POST
            db_response = insert_book(put_body)

            if db_response.error:
                status = 500
                response_body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
            else:
                status = 201
                links = LinkDto(request.path, 'books', request.method)
                response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
                response_body.set_links(links)

        else:
            # update happened, status will remain 200
            links = LinkDto(request.path, 'books', request.method)
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
            response_body.set_links(links)

    return jsonify(response_body.__dict__), status


@app.route('/api/bookcollection/authors/<author_id>', methods=['GET'])
def get_author(author_id):
    """
    Method that handles a GET request for an author by his id.

    :param author_id: id of the author that is to be retrieved
    """
    db_response = get_author_by_id(author_id)
    body = ''
    status = 200
    if db_response.error:
        status = 500
        body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status = 404
        body = AUTHOR_NOT_FOUND_BODY
    else:
        status = 200
        links = LinkDto(request.path, 'authors', request.method)
        body = AuthorDto(db_response.payload, links)

    return jsonify(body.__dict__), status


@app.route('/api/bookcollection/authors/<author_id>', methods=['DELETE'])
def delete_author(author_id):
    """
    Method that handles a DELETE request for an author by his id.

    :param author_id: id of the author that is to be deleted
    """
    db_response = delete_author_by_id(author_id)
    body = ''
    status = 200
    if db_response.error:
        status = 500
        body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
    elif not db_response.completed_operation:
        status = 404
        body = AUTHOR_NOT_FOUND_BODY
    else:
        status = 200
        links = LinkDto(request.path, 'authors', request.method)
        body = GENERIC_SUCCESS_STATUS_BODY
        body.set_links(links)

    return jsonify(body.__dict__), status


@app.route('/api/bookcollection/authors/', methods=['POST'])
def post_author():
    post_body = json.loads(request.get_data())
    is_valid, not_valid_reason = validate_author_post_or_put_body(post_body)
    status = 201
    response_body = ''

    if is_valid is not True:
        status = 400
        response_body = ErrorDto(400, not_valid_reason, 'INVALID_PARAMETERS')
    else:
        db_response = insert_author(post_body)

        if db_response.error:
            status = 500
            response_body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
        else:
            # TODO: reffer inserted author id somehow.
            links = LinkDto(request.path, 'authors', request.method)
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
            response_body.set_links(links)

    return jsonify(response_body.__dict__), status


@app.route('/api/bookcollection/authors/<author_id>', methods=['PATCH'])
def patch_author(author_id):
    put_body = json.loads(request.get_data())

    is_valid, not_valid_reason = validate_author_post_or_put_body(put_body)
    status = 200
    response_body = ''

    if is_valid is not True:
        status = 400
        response_body = ErrorDto(400, not_valid_reason, 'INVALID_PARAMETERS')
    else:
        db_response = update_author(author_id, put_body)

        if db_response.error:
            status = 500
            response_body = ErrorDto(500, str(db_response.error), 'EXCEPTION')
        elif db_response.completed_operation is False:
            # update did not succeed because there was no author with that id
            # will not try POST, because of the autoincrement feature of the author id
            status = 400
            response_body = ErrorDto(400,
                                     'Cannot continue with creation of the author if the author does not exist. '
                                     'Please use the POST method.',
                                     'INVALID_PARAMETERS')

        else:
            # update happened, status will remain 200
            links = LinkDto(request.path, 'books', request.method)
            response_body = CREATE_GENERIC_SUCCESS_STATUS_BODY
            response_body.set_links(links)

    return jsonify(response_body.__dict__), status


if __name__ == '__main__':
    app.run(debug=True)
