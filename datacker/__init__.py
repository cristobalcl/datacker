from typing import List
import tempfile
from pathlib import Path

import docker

from .images import build_dockerfile, build_directory, build_image
from .fs import LocalFileSystem


def build_datacker(name: str, notebooks: List[Path]):
    docker_client = docker.from_env()

    dockerfile = build_dockerfile(notebooks)
    with tempfile.TemporaryDirectory() as tmp_dir:
        working_dir = Path(tmp_dir)
        build_directory(
            notebooks, dockerfile, working_dir, LocalFileSystem(),
        )
        build_image(name, working_dir, docker_client.images)
