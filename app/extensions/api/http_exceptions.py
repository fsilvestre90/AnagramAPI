# encoding: utf-8
"""
HTTP exceptions collection
--------------------------
"""

from flask_restplus.errors import abort as utilities_abort
from utilities._http import HTTPStatus


API_DEFAULT_HTTP_CODE_MESSAGES = {
    HTTPStatus.UNPROCESSABLE_ENTITY.value: (
        "The request was well-formed but was unable to be followed due to semantic errors."
    ),
}


def abort(code, message=None, **kwargs):
    if message is None:
        if code in API_DEFAULT_HTTP_CODE_MESSAGES:
            message = API_DEFAULT_HTTP_CODE_MESSAGES[code]
        else:
            message = HTTPStatus(code).description
        utilities_abort(code=code, status=code, message=message, **kwargs)
