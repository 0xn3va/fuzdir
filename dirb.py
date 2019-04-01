from src.core.ArgumentParser import ArgumentParser
from src.core.Controller import Controller

from src.output.CLIOutput import CLIOutput


def dirb():
    output = CLIOutput()
    arg_parser = ArgumentParser(output=output)
    controller = Controller(output=output, arg_parser=arg_parser)
    controller.start()


if __name__ == '__main__':
    dirb()

