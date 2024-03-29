from requests import Response

from src.output.output import Output
from src.output.report.implement.plain_report import PlainReport
from src.output.report_manager import ReportManager
from src.output.report.report_type import ReportType

output = Output()
report = ReportManager()


def setup(config: tuple):
    report.setup(config)


def shutdown():
    report.shutdown()


def line(line: str):
    output.line(line)


def banner(banner: str):
    output.banner(banner)


def summary(log_path: str, threads: int, method: str, dictionary_size: int, target: str):
    output.summary(log_path, threads, method, dictionary_size, target)


def progress_bar(percent: float):
    output.progress_bar(percent)


def error(message: str):
    output.error(message)


def response(response: Response):
    output.response(response)
    report.write(response)
