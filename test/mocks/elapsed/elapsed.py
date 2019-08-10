import random

from test.utils.elapsed_mock.elapsed_modes import ElapsedModes


class Elapsed:
    _default_value = 0.001
    _default_delta = 0.025

    def __init__(self):
        self._value = self._default_value
        self.mode = ElapsedModes.stable

    def reset(self):
        self._value = self._random_value()
        self.mode = ElapsedModes.stable

    @property
    def value(self):
        if self.mode == ElapsedModes.stable:
            self._value = self._random_value()
        elif self.mode == ElapsedModes.increase:
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
