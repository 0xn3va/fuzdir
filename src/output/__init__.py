from requests import Response

from src.output.Output import Output

output = Output()


def line(line: str):
    output.line(line)


def progress_bar(percent: float):
    output.progress_bar(percent)


def error(message: str):
    output.error(message)


def response(response: Response):
    output.response(response)
