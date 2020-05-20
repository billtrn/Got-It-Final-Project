from flask import jsonify


class BaseError(Exception):
    """
    Base class for all exceptions
    """

    status_code = None
    message = None

    def __init__(self, message):
        super(BaseError).__init__()
        self.message = message

    def messages(self):
        return jsonify(description=self.message), self.status_code


class BadRequestError(BaseError):
    status_code = 400


class UnauthorizedError(BaseError):
    status_code = 401


class ForbiddenError(BaseError):
    status_code = 403


class NotFoundError(BaseError):
    status_code = 404
