import os


class FileUtils:

    @staticmethod
    def dir_exist(path: str):
        if not isinstance(path, str):
            return False
        return os.path.isdir(os.path.dirname(path))

    @staticmethod
    def is_writable(path: str):
        if not isinstance(path, str):
            return False
        return os.access(os.path.dirname(path), os.W_OK)

