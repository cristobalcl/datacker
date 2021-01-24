import os
import unittest
from unittest.mock import MagicMock
from pathlib import Path
import tempfile

import docker

from ..fs import FileSystemInterface
from ..builder import DatackerBuilder, DOCKER_BASE


docker_client = docker.from_env()


class FakeFileSystem(FileSystemInterface):
    def __init__(self):
        self.commands = []

    def write(self, filename: Path, content: str):
        self.commands.append(("WRITE", str(filename), content))

    def copy(self, source: Path, dest: Path):
        self.commands.append(("COPY", str(source), str(dest)))

    def delete(self, path: Path):
        # self.commands.append(("DELETE", str(path)))
        raise NotImplementedError  # pragma: no cover

    def create_temporal_directory(self) -> Path:
        # self.commands.append(("TEMPORAL DIR", "tmp/dir"))
        # return Path("tmp/dir")
        raise NotImplementedError  # pragma: no cover


class TestDatackerBuilder(unittest.TestCase):
    def test_build_empty_dockerfile(self):
        expected = f"FROM {DOCKER_BASE}"
        builder = DatackerBuilder("test_image", [], FakeFileSystem())
        dockerfile = builder._build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_one_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        builder = DatackerBuilder(
            "test_image", [Path("hello_world.ipynb")], FakeFileSystem()
        )
        dockerfile = builder._build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_remove_path_from_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        builder = DatackerBuilder(
            "test_image", [Path("path/to/hello_world.ipynb")], FakeFileSystem()
        )
        dockerfile = builder._build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_many_notebook(self):
        expected = [
            "ADD hello_world_1.ipynb /notebooks/",
            "ADD hello_world_2.ipynb /notebooks/",
        ]
        builder = DatackerBuilder(
            "test_image",
            [Path("hello_world_1.ipynb"), Path("hello_world_2.ipynb")],
            FakeFileSystem(),
        )
        dockerfile = builder._build_dockerfile().split("\n")
        for line in expected:
            self.assertIn(line, dockerfile)

    def test_build_directory(self):
        fs = FakeFileSystem()
        builder = DatackerBuilder(
            "test_image", [Path("notebook_1.ipynb"), Path("notebook_2.ipynb")], fs
        )
        builder._build_directory(
            dockerfile="FROM TEST_BASE_IMAGE", working_path=Path("path/to/tmp")
        )
        self.assertIn(("COPY", "notebook_1.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(("COPY", "notebook_2.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(
            ("WRITE", "path/to/tmp/Dockerfile", "FROM TEST_BASE_IMAGE"), fs.commands
        )

    def test_build_image(self):
        docker_client = MagicMock()
        builder = DatackerBuilder(
            "test_image",
            [Path("hello_world_1.ipynb"), Path("hello_world_2.ipynb")],
            FakeFileSystem(),
            docker_client=docker_client,
        )
        builder._build_image(working_path=Path("/tmp/test"))
        docker_client.images.build.called_with("/tmp/test", "test_image")

    def test_create_and_run_datacker(self):
        image_name = "datacker_test_create_image"
        notebooks = [
            Path(os.path.dirname(os.path.abspath(__file__)))
            / "notebooks"
            / "test.ipynb",
        ]
        builder = DatackerBuilder(image_name, notebooks)
        try:
            builder.build()

            docker_client.images.get(image_name)
            docker_client.containers.run(
                image_name, environment=dict(NOTEBOOK_NAME="test"),
            )
        finally:
            docker_client.images.remove(image_name, force=True)

    def test_create_with_dir(self):
        image_name = "datacker_test_create_image"
        notebooks = [
            Path(os.path.dirname(os.path.abspath(__file__)))
            / "notebooks"
            / "test.ipynb",
        ]
        builder = DatackerBuilder(image_name, notebooks)
        try:
            with tempfile.TemporaryDirectory() as working_dir:
                builder.build(working_dir=working_dir)

            docker_client.images.get(image_name)
            docker_client.containers.run(
                image_name, environment=dict(NOTEBOOK_NAME="test"),
            )
        finally:
            docker_client.images.remove(image_name, force=True)
