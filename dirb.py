import os

from src.core.ArgumentParser import ArgumentParser
from src.core.Controller import Controller

from src.output.CLIOutput import CLIOutput


def dirb():
    banner_path = os.path.join(os.path.dirname(__file__), 'banner.txt')
    output = CLIOutput()
    arg_parser = ArgumentParser(output=output)
    controller = Controller(banner_path=banner_path, output=output, arg_parser=arg_parser)
    controller.start()


if __name__ == '__main__':
    dirb()

