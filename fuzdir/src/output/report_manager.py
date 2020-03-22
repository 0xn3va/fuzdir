import logging
import threading

from src.output.report.implement.json_report import JsonReport
from src.output.report.implement.plain_report import PlainReport
from src.output.report.report_type import ReportType


class ReportManager:
    _handlers = {
        ReportType.plain: PlainReport,
        ReportType.json: JsonReport
    }

    def __init__(self):
        self._lock = threading.Lock()
        self._report = None

    def setup(self, config: tuple):
        if config is not None:
            with self._lock:
                if self._report is not None:
                    logging.warning('Shutdown is not called before reconfiguration')

                name, filename, components = config
                self._report = self._handlers[name](config, filename)

    def shutdown(self):
        with self._lock:
            if self._report is not None:
                self._report.close()
                self._report = None

    def write(self, *args):
        with self._lock:
            if self._report is not None:
                self._report.write(*args)
