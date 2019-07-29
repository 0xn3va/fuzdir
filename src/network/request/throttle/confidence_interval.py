import logging
from math import sqrt

from src.network.request.throttle.action import Action


class ConfidenceInterval:
    _window_size = 63
    _threshold = int(_window_size * 0.5)
    _min_mean = 0.05
    #
    _logging_format = 'Period: %.4f, borders: [%.4f, %.4f]'

    def __init__(self, period: float = None):
        self._fixed_period = period is not None
        self._period = period or 0.
        self._action = None
        # 3-sigma borders and counters
        self._borders = None
        # statistics
        self._count = 0
        self._mean = 0.
        self._variance = 0.

    def period(self, elapsed):
        if not self._fixed_period:
            if self._borders is None:
                if self._count < self._window_size:
                    self._statistics_update(elapsed)
                else:
                    left, right = self._three_sigma_borders()
                    self._borders = (left, right)
                    logging.debug(self._logging_format % (self._period, left, right))
            else:
                left, right = self._borders
                if elapsed < left:
                    action = Action.decrease
                elif elapsed > right:
                    action = Action.increase
                else:
                    action = None

                if self._action != action:
                    self._statistics_reset()
                    self._action = action

                if self._action is not None:
                    if self._count < self._threshold:
                        self._statistics_update(elapsed)
                    else:
                        if self._mean < self._min_mean:
                            self._period = 0.
                            self._borders = None
                        else:
                            self._period = self._mean
                            left, right = self._three_sigma_borders()
                            self._borders = (left, right)
                            logging.debug(self._logging_format % (self._period, left, right))
                        self._statistics_reset()
                        self._action = None
        return self._period

    def _statistics_update(self, elapsed):
        # Welford's algorithm
        self._count += 1
        delta = elapsed - self._mean
        self._mean += delta / self._count
        self._variance += (delta * (elapsed - self._mean) - self._variance) / self._count

    def _statistics_reset(self):
        self._count = 0
        self._mean = 0.
        self._variance = 0.

    def _three_sigma_borders(self):
        window = 3 * sqrt(self._variance)
        return self._mean - window, self._mean + window
