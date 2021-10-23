from flask import Flask, jsonify, request
from model import get_book_by_isbn
from datetime import datetime

app = Flask(__name__)


class ErrorDto:
    def __init__(self, error_code, error_reason, error_source):
        self.error_code = error_code
        self.error_reason = error_reason
        self.error_source = error_source
        self.timestamp = datetime.now()


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


@app.route('/api/bookcollection/books/<isbn>', methods=['GET'])
def get_book(isbn):
    """
    Method that handles a GET request for a book by the ISBN code.

    :param isbn: isbn code of the book that is to be retrieved
    """
    db_response = get_book_by_isbn(str(isbn))
    body = ''
    status = 200
    if db_response.erorr:
        status = 404
        body = ErrorDto(404, str(db_response.erorr), 'EXCEPTION')
    elif not db_response.completed_operation:
        status = 404
        body = ErrorDto(404, 'Requested book does not exist.', 'INVALID_OPERATION')
    else:
        status = 200
        links = LinkDto(request.path, 'books', request.method)
        body = BookDto(db_response.payload, links)

    return jsonify(body.__dict__), status


if __name__ == '__main__':
    app.run(debug=True)
