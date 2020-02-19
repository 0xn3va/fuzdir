import threading
from functools import wraps
from time import time, sleep

from src.network.requester.throttle.confidence_interval import ConfidenceInterval


class Throttle:
    def __init__(self, period: float = None):
        self._lock = threading.Lock()
        self._interval = ConfidenceInterval(period=period)
        self._time_of_last_call = None

    def __call__(self, request):
        @wraps(request)
        def wrap(*args, **kwargs):
            t = time()
            response = request(*args, **kwargs)
            self._throttle(time() - t)
            return response
        return wrap

    def _throttle(self, elapsed: float):
        with self._lock:
            period = self._interval.period(elapsed)
            self._delay(period)

    def _delay(self, period):
        current_time = time()
        if self._time_of_last_call is None:
            self._time_of_last_call = current_time
        else:
            time_since_last_call = current_time - self._time_of_last_call
            if time_since_last_call < period:
                delta = period - time_since_last_call
                sleep(delta)
                self._time_of_last_call = time()
            else:
                self._time_of_last_call = current_time
