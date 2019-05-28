import os


class FileUtils:

    @staticmethod
    def dir_exist(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.path.isdir(FileUtils.dirname(path))

    @staticmethod
    def is_writable(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.access(FileUtils.dirname(path), os.W_OK) and not os.path.isdir(path)

    @staticmethod
    def is_readable(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.path.isfile(path) and os.access(FileUtils.dirname(path), os.R_OK)

    @staticmethod
    def dirname(path: str) -> str:
        return os.path.dirname(os.path.abspath(path))
