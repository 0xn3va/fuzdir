import os
from pathlib import Path


class FileUtils:
    @staticmethod
    def is_writable(path) -> bool:
        if isinstance(path, str):
            path = Path(path)
        # is_writable consider a file missing
        return os.access(FileUtils.dirname(path), os.W_OK) and (not path.exists() or path.is_file() and os.access(path, os.W_OK))

    @staticmethod
    def is_readable(path) -> bool:
        if isinstance(path, str):
            path = Path(path)
        return os.access(path, os.R_OK) and path.is_file()

    @staticmethod
    def dirname(path: Path) -> str:
        return path.resolve().parent
