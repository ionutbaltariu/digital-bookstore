from books import Book
from authors import Author
from books_authors import BooksAuthors
from db import Session, engine

local_session = Session(bind=engine)


def get_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is retrieving a book by its ISBN.

    :param isbn: isbn code of the book that is to be retrieved
    """
    response = OperationResponseWrapper()
    try:
        response.payload = local_session.query(Book).filter(Book.isbn == isbn).first()
        if not response.payload:
            response.completed_operation = False
        else:
            response.completed_operation = True
    except Exception as e:
        response.erorr = e
        response.completed_operation = False

    return response


def delete_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is deleting a book by its ISBN.

    :param isbn: isbn code of the book that is to be deleted
    """
    response = OperationResponseWrapper()

    try:
        book_to_delete = local_session.query(Book).filter(Book.isbn == isbn).first()

        if book_to_delete:
            local_session.delete(book_to_delete)
            local_session.commit()
        else:
            response.completed_operation = False

    except Exception as e:
        response.completed_operation = False
        response.erorr = e

    return response


def insert_book(book):
    """
    Wrapper for an ORM call that inserts a book into the database.

    :param book: a dictionary containing the book's fields
    """
    response = OperationResponseWrapper()

    book_to_insert = Book(isbn=book['isbn'],
                          title=book['title'],
                          publisher=book['publisher'],
                          year_of_publishing=book['year_of_publishing'],
                          genre=book['genre'])
    try:
        local_session.add(book_to_insert)
        local_session.commit()
        response.completed_operation = True
        response.payload = book_to_insert
    except Exception as e:
        response.completed_operation = False
        response.erorr = True


def update_book(isbn, book):
    """
        Wrapper for an ORM call that updates a book from the database.

        :param isbn: isbn code of the book that is to be updated
        :param book: a dictionary containing the book's fields - can be partial
        """
    response = OperationResponseWrapper()

    try:
        book_to_update = local_session.query(Book).filter(Book.isbn == isbn).first()

        for field in book:
            setattr(book_to_update, field, book[field])

        local_session.add(book_to_update)
        local_session.commit()
        response.completed_operation = True
        response.payload = book_to_update
    except Exception as e:
        response.completed_operation = False
        response.erorr = e

    return response


class OperationResponseWrapper:
    def __init__(self, payload=None, error=None, completed_operation=True):
        self.payload = payload
        self.erorr = error
        self.completed_operation = completed_operation
