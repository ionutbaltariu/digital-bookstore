from datetime import datetime


class ErrorDto:
    def __init__(self, error_code, error_reason, error_source):
        self.error_code = error_code
        self.error_reason = error_reason
        self.error_source = error_source
        self.timestamp = datetime.now()


class StatusDto:
    def __init__(self, code, message):
        self.code = code
        self.message = message
        self.links = None

    def set_links(self, links):
        self.links = links.__dict__


# used in GET, DELETE when a requested book does not actually exist.
BOOK_NOT_FOUND_BODY = ErrorDto(404, 'Requested book does not exist.', 'INVALID_OPERATION')
GENERIC_SUCCESS_STATUS_BODY = StatusDto(200, 'Operation was completed successfully.')
CREATE_GENERIC_SUCCESS_STATUS_BODY = StatusDto(201, 'Operation was completed successfully.')
AUTHOR_NOT_FOUND_BODY = ErrorDto(404, 'Requested author does not exist', 'INVALID_OPERATION')
