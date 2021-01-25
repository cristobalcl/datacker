from typing import List, Optional
from pathlib import Path

import docker

from .fs import FileSystemInterface, LocalFileSystem


DOCKER_BASE = "cristobalcl/datacker"


class DatackerBuilder:
    fs: FileSystemInterface

    def __init__(
        self,
        name: str,
        notebooks: List[str],
        requirements_file: Optional[str] = None,
        fs: Optional[FileSystemInterface] = None,
        docker_client=None,
    ):
        self.name = name
        self.notebooks = [Path(notebook) for notebook in notebooks]
        self.requirements_path = (
            Path(requirements_file) if requirements_file is not None else None
        )
        if fs is None:
            self.fs = LocalFileSystem()  # pragma: no cover
        else:
            self.fs = fs
        if docker_client is None:
            self.docker_client = docker.from_env()
        else:
            self.docker_client = docker_client

    def _build_dockerfile(self) -> str:
        dockerfile = [f"FROM {DOCKER_BASE}"]
        if self.requirements_path is not None:
            dockerfile.append(f"ADD {self.requirements_path.parts[-1]} /")
            dockerfile.append(f"RUN pip install -r {self.requirements_path.parts[-1]}")
        for notebook in self.notebooks:
            notebook_filename = notebook.parts[-1]
            dockerfile.append(f"ADD {notebook_filename} /notebooks/")
        return "\n".join(dockerfile)

    def _build_directory(self, dockerfile: str, working_path: Path):
        self.fs.write(working_path / "Dockerfile", dockerfile)
        if self.requirements_path is not None:
            self.fs.copy(self.requirements_path, working_path)
        for notebook in self.notebooks:
            self.fs.copy(notebook, working_path)

    def _build_image(self, working_path: Path):
        self.docker_client.images.build(path=str(working_path), tag=self.name)

    def build(self, working_dir: Optional[str] = None):
        dockerfile = self._build_dockerfile()
        if working_dir is not None:
            working_path = Path(working_dir)
        else:
            working_path = self.fs.create_temporary_directory()
        try:
            self._build_directory(dockerfile, working_path)
            self._build_image(working_path)
        finally:
            if working_dir is None:
                self.fs.delete(working_path)
