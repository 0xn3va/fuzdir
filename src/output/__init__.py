from requests import Response

from src.output.Output import Output
from src.output.reports.PlainReport import PlainReport
from src.output.reports.ReportManager import ReportManager
from src.output.reports.ReportType import ReportType
from src.output.SplashType import SplashType

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
