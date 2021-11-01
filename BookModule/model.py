from books import Book
from authors import Author
from books_authors import BooksAuthors
from db import Session, engine
import json

local_session = Session(bind=engine)

def get_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is retrieving a book by its ISBN.

    :param isbn: isbn code of the book that is to be retrieved
    """
    return get_entity_by_identifier(Book, 'isbn', isbn)


def delete_book_by_isbn(isbn):
    """
    Wrapper for an ORM call that is deleting a book by its ISBN.

    :param isbn: isbn code of the book that is to be deleted
    """
    return delete_entity_by_identifier(Book, 'isbn', isbn)


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
        local_session.rollback()
        response.completed_operation = False
        response.error = e

    return response


def update_book(isbn, book):
    """
        Wrapper for an ORM call that updates a book from the database.

        :param isbn: isbn code of the book that is to be updated
        :param book: a dictionary containing the book's fields - can be partial
        """
    return update_entity_by_identifier(Book, 'isbn', isbn, book)


def get_author_by_id(author_id):
    """
    Wrapper for an ORM call that is retrieving an author by his id.

    :param author_id: the id of the author
    """
    return get_entity_by_identifier(Author, 'id', author_id)


def insert_author(author):
    """
    Wrapper for an ORM call that inserts an author into the database.

    :param author: a dictionary containing the author's fields
    """
    response = OperationResponseWrapper()

    author_to_insert = Author(first_name=author['first_name'],
                              last_name=author['last_name'])

    try:
        local_session.add(author_to_insert)
        local_session.commit()
        response.completed_operation = True
        response.payload = author_to_insert
    except Exception as e:
        local_session.rollback()
        response.completed_operation = False
        response.error = e

    return response


def delete_author_by_id(author_id):
    """
    Wrapper for an ORM call that is deleting an author by its id.

    :param author_id: id of the author that is to be deleted
    """
    return delete_entity_by_identifier(Author, 'id', author_id)


def update_author(author_id, author):
    """
    Wrapper for an ORM call that is updating an author by its id.

    :param author_id: id of the author that is to be deleted
    :param author: a dictionary containing the fields to be updated
    """
    return update_entity_by_identifier(Author, 'id', author_id, author)


def delete_entity_by_identifier(entity, identifier_name, identifier_value):
    """
    Wrapper for a generic ORM call that is deleting an Entity by an identifier.

    :param entity: the type of the entity that is to be deleted
    :param identifier_name: the column/field by which the identifier will be searched and deleted
    :param identifier_value: the value of the identifier column
    """
    response = OperationResponseWrapper()

    try:
        entity_to_delete = local_session.query(entity).filter(
            getattr(entity, identifier_name) == identifier_value).first()

        if entity_to_delete:
            local_session.delete(entity_to_delete)
            local_session.commit()
        else:
            response.completed_operation = False

    except Exception as e:
        response.completed_operation = False
        response.error = e

    return response


def get_entity_by_identifier(entity, identifier_name, identifier_value):
    """
    Wrapper for a generic ORM call that is retrieving an Entity by an identifier.

    :param entity: the type of the entity that is to be retrieved
    :param identifier_name: the column/field by which the identifier will be searched
    :param identifier_value: the value of the identifier column
    """
    response = OperationResponseWrapper()
    try:
        response.payload = local_session.query(entity).filter(
            getattr(entity, identifier_name) == identifier_value).first()
        if not response.payload:
            response.completed_operation = False
        else:
            response.completed_operation = True
    except Exception as e:
        response.error = e
        response.completed_operation = False

    return response


def update_entity_by_identifier(entity, identifier_name, identifier_value, updated_entity_fields):
    """
    Wrapper for a generic ORM call that is updating an Entity by an identifier.

    :param entity: the type of the entity that is to be updated
    :param identifier_name: the column/field by which the identifier will be searched
    :param identifier_value: the value of the identifier column
    :param updated_entity_fields: a dictionary that contains the new values of the entity
    """
    response = OperationResponseWrapper()

    try:
        entity_to_update = local_session.query(entity).filter(
            getattr(entity, identifier_name) == identifier_value).first()

        if entity_to_update:
            for field in updated_entity_fields:
                setattr(entity_to_update, field, updated_entity_fields[field])

            local_session.add(entity_to_update)
            local_session.commit()
            response.completed_operation = True
            response.payload = entity_to_update
        else:
            response.completed_operation = False
    except Exception as e:
        local_session.rollback()
        response.completed_operation = False
        response.error = e

    return response


def get_all_entities(entity, **kwargs):
    """
    Wrapper for a generic ORM call that is retrieving all instances of
    any entity also using some filter parameters.

    :param entity: the type of the entity that is to be retrieved
    :param kwargs: the parameters by which the filters will be made
    """
    response = OperationResponseWrapper()

    try:
        response.payload = local_session.query(entity).filter_by(**kwargs).all()
        response.completed_operation = True
    except Exception as e:
        response.error = e
        response.completed_operation = False

    return response


def get_all_books_with_filters(**kwargs):
    """
    Wrapper for an ORM call that is retrieving all books by some filters.

    :param kwargs: the parameters by which the filters will be made
    """
    return get_all_entities(Book, **kwargs)


def get_all_authors_with_filters(**kwargs):
    """
    Wrapper for an ORM call that is retrieving all the authors by some filters.

    :param kwargs: the parameters by which the filters will be made
    """
    return get_all_entities(Author, **kwargs)


class OperationResponseWrapper:
    def __init__(self, payload=None, error=None, completed_operation=True):
        self.payload = payload
        self.error = error
        self.completed_operation = completed_operation