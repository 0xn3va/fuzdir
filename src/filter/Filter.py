from src.filter.Code import Code


class Filter:
    handlers = {
        'code': Code
    }

    def __init__(self, conditions: str = '', invert: bool = False):
        self._conditions = []

        # -x code=200,301 : filter key
        # -v : invert key

        for condition in conditions.split(';'):
            try:
                name_args = condition.split('=')
                if len(name_args) != 2:
                    # todo('raise exception')
                    pass

                name, args = name_args

                handler = self.handlers[name]()
                handler.setup(args.split(','))
                self._conditions.append(handler)
            except KeyError:
                # todo('raise exception')
                return
