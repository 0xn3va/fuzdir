import threading

from src.output.reports.plain_report import PlainReport
from src.output.reports.report_type import ReportType


class ReportManager:

    def __init__(self):
        self._lock = threading.Lock()
        self._report = None

    def config(self, report_type: ReportType, filename: str):
        # shutdown method must be called for reconfig
        with self._lock:
            if report_type == ReportType.plain_text:
                self._report = PlainReport(filename)

    def shutdown(self):
        with self._lock:
            if self._report is not None:
                self._report.close()
                self._report = None

    def write(self, *args):
        with self._lock:
            if self._report is not None:
                self._report.write(*args)
