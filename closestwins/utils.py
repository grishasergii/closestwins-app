"""Closest wins app utils."""

from functools import wraps
from http import HTTPStatus

from flask import abort


def disable(_f):
    """Disable route decorator."""
    @wraps(_f)
    def decorated_function(*_args, **_kwargs):
        return abort(HTTPStatus.NOT_FOUND)

    return decorated_function
