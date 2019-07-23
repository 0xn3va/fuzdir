from requests import Response

from src.output.Output import Output
from src.output.SplashType import SplashType

output = Output()


def line(line: str):
    output.line(line)


def splash(splash_type: SplashType, *args):
    output.splash(splash_type, *args)


def progress_bar(percent: float):
    output.progress_bar(percent)


def error(message: str):
    output.error(message)


def response(response: Response):
    output.response(response)
