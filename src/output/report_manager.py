import threading

from src.output.report.implement.plain_report import PlainReport
from src.output.report.report_type import ReportType


class ReportManager:
    _handlers = {
        ReportType.plain_text: PlainReport
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._report = None

    def config(self, report_type: ReportType, filename: str):
        # shutdown method must be called for reconfig
        with self._lock:
            self._report = self._handlers[report_type](filename)

    def shutdown(self):
        with self._lock:
            if self._report is not None:
                self._report.close()
                self._report = None

    def write(self, *args):
        with self._lock:
            if self._report is not None:
                self._report.write(*args)
