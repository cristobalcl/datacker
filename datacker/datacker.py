from typing import List, Optional

import shutil
import tempfile
from pathlib import Path

# from icecream import ic

import docker


docker_client = docker.from_env()

DOCKER_BASE = "cristobalcl/datacker"


def build_dockerfile(notebooks: Optional[List[str]] = None) -> str:
    notebooks = notebooks or []
    dockerfile = [f"FROM {DOCKER_BASE}"]
    for notebook in notebooks:
        dockerfile.append(f"ADD {notebook} /notebooks/")
    return "\n".join(dockerfile)


def create_image(name: str, notebooks: Optional[List[str]] = None):
    notebooks = notebooks or []
    tmp_dir = Path(tempfile.mkdtemp())
    try:
        with (tmp_dir / "Dockerfile").open("w") as f:
            f.write(
                build_dockerfile([Path(notebook).parts[0] for notebook in notebooks])
            )
        for notebook in notebooks:
            shutil.copy(notebook, tmp_dir)
        image, _logs = docker_client.images.build(path=str(tmp_dir), tag=name)
    finally:
        shutil.rmtree(tmp_dir)
