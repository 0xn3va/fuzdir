import os


class FileUtils:

    @staticmethod
    def is_writable(path: str) -> bool:
        # is_writable consider a file missing
        return os.access(FileUtils.dirname(path), os.W_OK) and \
               (not os.path.exists(path) or os.path.isfile(path) and os.access(path, os.W_OK))

    @staticmethod
    def is_readable(path: str) -> bool:
        return os.access(path, os.R_OK) and os.path.isfile(path)

    @staticmethod
    def dirname(path: str) -> str:
        return os.path.dirname(os.path.abspath(path))
