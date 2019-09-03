import warnings


def ignore_resource_warning(func):
    def wrap(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', ResourceWarning)
            func(self, *args, **kwargs)

    return wrap
