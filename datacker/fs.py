from abc import ABC, abstractmethod
from typing import Optional
import shutil
import tempfile
from pathlib import Path


class FileSystemInterface(ABC):
    @abstractmethod
    def write(self, filename: Path, content: str):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def copy(self, source: Path, dest: Path):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def delete(self, path: Path):
        raise NotImplementedError  # pragma: no cover

    @abstractmethod
    def create_temporary_directory(self) -> Path:
        raise NotImplementedError  # pragma: no cover


class LocalFileSystem(FileSystemInterface):
    def write(self, filename: Path, content: str):
        with open(str(filename), "w") as f:
            f.write(content)

    def copy(self, source: Path, dest: Path):
        shutil.copy(source, dest)

    def delete(self, path: Path):
        shutil.rmtree(path)

    def create_temporary_directory(self, prefix: Optional[str] = None) -> Path:
        return Path(tempfile.mkdtemp(prefix=prefix))
