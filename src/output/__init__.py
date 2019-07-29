from requests import Response

from src.output.output import Output
from src.output.reports.plain_report import PlainReport
from src.output.reports.report_manager import ReportManager
from src.output.reports.report_type import ReportType
from src.output.splash_type import SplashType

output = Output()
report = ReportManager()


def config(report_type: ReportType, filename: str):
    report.config(report_type, filename)


def shutdown():
    report.shutdown()


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
    report.write(response)
