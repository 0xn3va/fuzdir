import random

from test.mocks.elapsed.elapsed_mock_modes import ElapsedMockModes


class ElapsedMock:
    _default_value = 0.001
    _default_delta = 0.025

    def __init__(self):
        self._value = self._default_value
        self.mode = ElapsedMockModes.stable

    def reset(self):
        self._value = self._random_value()
        self.mode = ElapsedMockModes.stable

    @property
    def value(self):
        if self.mode == ElapsedMockModes.stable:
            self._value = self._random_value()
        elif self.mode == ElapsedMockModes.increase:
            self._value += self._random_delta()
        else:
            self._value -= self._random_delta()
            if self._value < 0:
                self._value = self._random_value()
        return self._value

    def _random_value(self):
        return self._default_value + random.random() / 1000.

    def _random_delta(self):
        return self._default_delta + random.random() / 100.
