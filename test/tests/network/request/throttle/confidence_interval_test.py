import random
import unittest

from src.network.request.throttle.confidence_interval import ConfidenceInterval
from test.utils.elapsed_mock.elapsed import Elapsed
from test.utils.elapsed_mock.elapsed_modes import ElapsedModes


class ConfidenceIntervalTest(unittest.TestCase):
    _stable_iterations = 2 * ConfidenceInterval._window_size
    _changeable_iterations = 6 * ConfidenceInterval._window_size
    _elapsed = Elapsed()

    def test_period_fixed(self):
        self._elapsed.reset()
        period = 10 * random.random()
        confidence_interval = ConfidenceInterval(period=period)
        for _ in range(self._stable_iterations):
            self.assertEqual(confidence_interval.period(self._elapsed.value), period,
                             msg='Check on a fixed period failed')

    def test_period_smoothly_delay(self):
        self._elapsed.reset()
        confidence_interval = ConfidenceInterval()
        period = None
        # stable
        for _ in range(self._stable_iterations):
            period = confidence_interval.period(self._elapsed.value)
        self.assertEqual(period, 0., msg='Check for no delays failed')
        # increase
        self._elapsed.mode = ElapsedModes.increase
        for _ in range(self._changeable_iterations):
            p = confidence_interval.period(self._elapsed.value)
            if p != period:
                if period is not None:
                    self.assertLess(period, p, msg='Check for increasing delays failed')
                period = p
        # decrease
        self._elapsed.mode = ElapsedModes.decrease
        for _ in range(self._changeable_iterations):
            p = confidence_interval.period(self._elapsed.value)
            if p != period:
                self.assertGreater(period, p, msg='Check for decreasing delays failed')
                period = p
        # stable
        self._elapsed.mode = ElapsedModes.stable
        for _ in range(self._stable_iterations):
            period = confidence_interval.period(self._elapsed.value)
        self.assertEqual(period, 0., msg='Check to return to initial state failed')
