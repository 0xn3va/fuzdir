import os


class FileUtils:

    @staticmethod
    def dir_exist(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.path.isdir(os.path.dirname(path))

    @staticmethod
    def is_writable(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.path.isfile(path) and os.access(os.path.dirname(path), os.W_OK)


    @staticmethod
    def is_readable(path: str) -> bool:
        if not isinstance(path, str):
            return False
        return os.path.isfile(path) and os.access(os.path.dirname(path), os.R_OK)
