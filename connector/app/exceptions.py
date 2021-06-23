from http import HTTPStatus

from fastapi import HTTPException


class NodeConnectionError(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs.update(status_code=HTTPStatus.SERVICE_UNAVAILABLE)

        super().__init__(*args, **kwargs)


class GroupNotFoundError(HTTPException):
    def __init__(self, *args, **kwargs):
        kwargs.update(status_code=HTTPStatus.NOT_FOUND)

        super().__init__(*args, **kwargs)
