from src.network.response.ResponseType import ResponseType


class Response:
    def __init__(self, type: ResponseType, body):
        self.type = type
        self.body = body
