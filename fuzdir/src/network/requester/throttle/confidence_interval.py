from logging import debug
from math import sqrt

from src.network.requester.throttle.action import Action


class ConfidenceInterval:
    _window_size = 63
    _threshold = int(_window_size * 0.5)
    _min_mean = 0.03

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
                    self._update(period=0.)
            else:
                left, right = self._borders
                if elapsed < left or left < 0. and self._mean < self._period:
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
                            self._update(period=self._mean)
                        self._statistics_reset()
                        self._action = None
        return self._period

    def _statistics_update(self, elapsed):
        # Welford's algorithm
        self._count += 1
        count_reverse = 1 / self._count
        delta = elapsed - self._mean
        self._mean += delta * count_reverse
        self._variance += (delta * (elapsed - self._mean) - self._variance) * count_reverse

    def _statistics_reset(self):
        self._count = 0
        self._mean = 0.
        self._variance = 0.

    def _update(self, period):
        self._period = period
        left, right = self._three_sigma_borders()
        self._borders = (left, right)
        debug(f'Changed period: {self._period:.4f}, borders: [{left:.4f}, {right:.4f}]')

    def _three_sigma_borders(self):
        window = 3 * sqrt(self._variance)
        return self._mean - window, self._mean + window
