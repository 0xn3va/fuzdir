from enum import Enum


class MessageType(Enum):
    response = 0,
    error = 1


class Message:
    def __init__(self, type: MessageType, body):
        self.type = type
        self.body = body
