from typing import List
from pathlib import Path

# from icecream import ic

from .fs import FileSystemInterface


DOCKER_BASE = "cristobalcl/datacker"


def build_dockerfile(notebooks: List[Path]) -> str:
    dockerfile = [f"FROM {DOCKER_BASE}"]
    for notebook in notebooks:
        notebook_filename = notebook.parts[-1]
        dockerfile.append(f"ADD {notebook_filename} /notebooks/")
    return "\n".join(dockerfile)


def build_directory(
    notebooks: List[Path], dockerfile: str, working_dir: Path, fs: FileSystemInterface
):
    fs.write(working_dir / "Dockerfile", dockerfile)
    for notebook in notebooks:
        fs.copy(notebook, working_dir)


def build_image(name: str, working_dir: Path, docker_client_images):
    docker_client_images.build(path=str(working_dir), tag=name)
