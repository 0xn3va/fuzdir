from src.network.response.response_type import ResponseType


class Response:
    def __init__(self, type: ResponseType, body):
        self.type = type
        self.body = body
