from enum import Enum


class ResponseType(Enum):
    response = 0,
    error = 1


class Response:
    def __init__(self, type: ResponseType, body):
        self.type = type
        self.body = body
