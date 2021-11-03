from datetime import datetime

# used in GET, DELETE when a requested book does not actually exist.
BOOK_NOT_FOUND_BODY = {
    "error_code": 404,
    "error_source": 'Requested book does not exist.',
    "error_reason": 'NONEXISTENT_RESOURCE'
}
GENERIC_SUCCESS_STATUS_BODY = {
    'code': 200,
    'message': 'Operation was completed successfully.'
}
CREATE_GENERIC_SUCCESS_STATUS_BODY = {
    'code': 201,
    'message': 'Operation was completed successfully.'
}
AUTHOR_NOT_FOUND_BODY = {
    "error_code": 404,
    "error_source": 'Requested author does not exist',
    "error_reason": 'NONEXISTENT_RESOURCE'
}


def get_error_body(code, source, reason):
    return {
        "error_code": code,
        "error_source": source,
        "error_reason": reason
    }
