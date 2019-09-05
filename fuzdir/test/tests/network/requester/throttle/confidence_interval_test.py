import random
import unittest

from fuzdir.src.network.requester import ConfidenceInterval
from fuzdir.test.mocks.elapsed.elapsed_mock import ElapsedMock
from fuzdir.test.mocks.elapsed.elapsed_mock_modes import ElapsedMockModes


class ConfidenceIntervalTest(unittest.TestCase):
    _stable_iterations = 2 * ConfidenceInterval._window_size
    _changeable_iterations = 6 * ConfidenceInterval._window_size
    _elapsed = ElapsedMock()

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
            self.assertEqual(period, 0., msg='Check for no delay failed')
        # increase
        self._elapsed.mode = ElapsedMockModes.increase
        is_changed = False
        for _ in range(self._changeable_iterations):
            p = confidence_interval.period(self._elapsed.value)
            if p != period:
                is_changed = True
                self.assertLess(period, p, msg='Check for increasing delay failed')
                period = p
        self.assertTrue(is_changed, msg='Check for increasing delay failed')
        # decrease
        self._elapsed.mode = ElapsedMockModes.decrease
        is_changed = False
        for _ in range(self._changeable_iterations):
            p = confidence_interval.period(self._elapsed.value)
            if p != period:
                is_changed = True
                self.assertGreater(period, p, msg='Check for decreasing delay failed')
                period = p
        self.assertTrue(is_changed, msg='Check for decreasing delay failed')
        # stable
        self._elapsed.mode = ElapsedMockModes.stable
        for _ in range(self._stable_iterations):
            period = confidence_interval.period(self._elapsed.value)
        self.assertEqual(period, 0., msg='Check to return to initial state failed')
