import argparse


class StoreList(argparse.Action):
    _separator = ','

    def __call__(self, parser, namespace, values, option_string=None):
        for value in values.split(self._separator):
            getattr(namespace, self.dest).append(value.strip())
