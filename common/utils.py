import logging
import sys


HTTP_STATUS_CODES = {
    "ok": 200,
    "created": 201,
    "bad_request": 400,
    "unauthorized": 401,
    "not_found": 404,
    "internal_server_error": 500
}


def setup_logging():
    """
    Method responsible for setting the logging to stderr
    """
    logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class ValidationError(Exception):
    """
    Validation data error
    """
    pass


class NotJsonFileError(Exception):
    """
    Not json file provided error
    """
    pass


class RecordNotFound(Exception):
    """
    Record not found in the database
    """
    pass
