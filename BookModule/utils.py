from datetime import datetime
from isbnlib import is_isbn10, is_isbn13, canonical


def validate_patch_body(body):
    """
    Validates a PATCH request body for the /books/{isbn} endpoint.

    :param body: The body of the request
    """
    is_valid = True
    reason = ''
    allowed_fields = ['isbn', 'title', 'publisher', 'year_of_publishing', 'genre']

    if len(body) == 0:
        is_valid = False
        reason = 'Empty body given.'

    if is_valid is True:
        for field in body:
            if field not in allowed_fields:
                is_valid = False
                reason = f"Body contains an unknown field: '{field}'"
                break

    if is_valid is True:
        is_valid, reason = check_if_all_fields_are_completed(body)

    if is_valid is True:
        if 'isbn' in body:
            is_valid = False
            reason = 'When updating, do not give the ISBN field.'

    if is_valid is True:
        if 'year_of_publishing' in body:
            is_valid, reason = check_year_of_publishing_validity(body['year_of_publishing'])

    return is_valid, reason


def validate_book_post_or_put_body(body):
    """
    Validates a POST or PUT request body for the /books  or /books/{isbn} endpoint.

    :param body: The body of the POST / PUT request

    Should have the form: \n
    {
        "isbn" : "str", \n
        "title" : "str", \n
        "publisher" : "str", \n
        "year_of_publishing" : int, \n
        "genre" : "str"
    }
    """
    is_valid = True
    reason = ''
    mandatory_fields = ['isbn', 'title', 'publisher', 'year_of_publishing', 'genre']

    for field in mandatory_fields:
        if field not in body:
            is_valid = False
            reason = f"Field '{field}' is mandatory. Please include it in the body of the request."
            break

    if is_valid is True:
        for field in body:
            if field not in mandatory_fields:
                is_valid = False
                reason = f"Body contains an unknown field: '{field}'"
                break

    if is_valid is True:
        is_valid, reason = check_if_all_fields_are_completed(body)

    year_of_publishing = body['year_of_publishing']

    if is_valid is True:
        is_valid, reason = check_year_of_publishing_validity(year_of_publishing)

    if is_valid is True:
        is_valid, reason = check_isbn_validity(body['isbn'])

    return is_valid, reason


def validate_author_post_or_put_body(body):
    """
    Validates a POST or PUT request body for the /authors  or /authors/{id} endpoint.

    :param body: The body of the POST / PUT request

    Should have the form: \n
    {
        "first_name" : "str", \n
        "last_name" : "str"
    }
    """
    is_valid = True
    reason = ''
    mandatory_fields = ['first_name', 'last_name']

    for field in mandatory_fields:
        if field not in body:
            is_valid = False
            reason = f"Field '{field}' is mandatory. Please include it in the body of the request."
            break

    if is_valid is True:
        is_valid, reason = check_if_all_fields_are_completed(body)

    if is_valid is True:
        for field in body:
            if field not in mandatory_fields and field != 'id':
                is_valid = False
                reason = f"Body contains an unknown field: '{field}'"
                break

    return is_valid, reason


def check_if_all_fields_are_completed(body):
    """
    Checks whether all the fields of the body were completed / len(field) > 0

    :param body: The body of the request
    """
    is_valid = True
    reason = ''

    for field in body:
        if len(str(body[field]).strip()) < 1:
            is_valid = False
            reason = f"Field '{field}' has an empty value. Please complete the value accordingly."
            break

    return is_valid, reason


def check_year_of_publishing_validity(year_of_publishing):
    """
    Checks if the year of publishing is valid / 0 <= year_of_publishing < current_year

    :param year_of_publishing: The year of publishing of the book
    """
    is_valid = True
    reason = ''

    if not isinstance(year_of_publishing, int):
        is_valid = False
        reason = f"Field 'year_of_publishing' should be an Integer."
    else:
        current_year = int(datetime.now().year)
        if year_of_publishing < 0 or year_of_publishing > current_year:
            is_valid = False
            reason = f"Field 'year_of_publishing' should have a value between 0 and {current_year}"

    return is_valid, reason


def check_isbn_validity(isbn):
    """
    Checks whether a given ISBN is valid or not.

    :param isbn: The ISBN of the book
    """
    is_valid = True
    reason = ''

    try:
        canonical_isbn = canonical(isbn)

        if (is_isbn13(canonical_isbn) is False) and (is_isbn10(canonical_isbn) is False):
            is_valid = False
            reason = f"{isbn} is not a valid ISBN-10 or ISBN-13."
    except Exception as e:
        is_valid = False
        reason = f"Invalid type for the ISBN."

    return is_valid, reason
