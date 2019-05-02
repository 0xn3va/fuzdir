import os

from src.core.Controller import Controller


def dirb():
    controller = Controller(root_path=os.path.abspath(os.path.dirname(__file__)))
    controller.start()


if __name__ == '__main__':
    dirb()

