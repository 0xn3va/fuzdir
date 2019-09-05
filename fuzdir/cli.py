from fuzdir import root_path
from src.core.controller import Controller


def main():
    controller = Controller(root_path=root_path)
    controller.start()
