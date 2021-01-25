import unittest
from unittest.mock import MagicMock
from pathlib import Path

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
        self.commands.append(("DELETE", str(path)))

    def create_temporary_directory(self) -> Path:
        self.commands.append(("TEMPORARY DIR", "fake/tmp/dir"))
        return Path("fake/tmp/dir")


class TestDatackerBuilder(unittest.TestCase):
    def test_build_empty_dockerfile(self):
        expected = f"FROM {DOCKER_BASE}"
        builder = DatackerBuilder("test_image", [], fs=FakeFileSystem())
        dockerfile = builder._build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_one_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        builder = DatackerBuilder(
            "test_image", [Path("hello_world.ipynb")], fs=FakeFileSystem()
        )
        dockerfile = builder._build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_remove_path_from_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        builder = DatackerBuilder(
            "test_image", [Path("path/to/hello_world.ipynb")], fs=FakeFileSystem()
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
            fs=FakeFileSystem(),
        )
        dockerfile = builder._build_dockerfile().split("\n")
        for line in expected:
            self.assertIn(line, dockerfile)

    def test_add_requirements(self):
        expected_lines = [
            "ADD req.txt /",
            "RUN pip install -r req.txt",
        ]
        builder = DatackerBuilder(
            "test_image",
            [Path("hello_world.ipynb")],
            requirements_file="path/to/req.txt",
            fs=FakeFileSystem(),
        )
        dockerfile = builder._build_dockerfile().split("\n")
        for line in expected_lines:
            self.assertIn(line, dockerfile)

    def test_build_directory(self):
        fs = FakeFileSystem()
        builder = DatackerBuilder(
            "test_image", [Path("notebook_1.ipynb"), Path("notebook_2.ipynb")], fs=fs
        )
        builder._build_directory(
            dockerfile="FROM TEST_BASE_IMAGE", working_path=Path("path/to/tmp")
        )
        self.assertIn(("COPY", "notebook_1.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(("COPY", "notebook_2.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(
            ("WRITE", "path/to/tmp/Dockerfile", "FROM TEST_BASE_IMAGE"), fs.commands
        )

    def test_build_directory_with_requirements(self):
        fs = FakeFileSystem()
        builder = DatackerBuilder(
            "test_image",
            [Path("notebook_1.ipynb"), Path("notebook_2.ipynb")],
            requirements_file="path/to/requirements.txt",
            fs=fs,
        )
        builder._build_directory(
            dockerfile="FROM TEST_BASE_IMAGE", working_path=Path("path/to/tmp")
        )
        self.assertIn(("COPY", "notebook_1.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(("COPY", "notebook_2.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(("COPY", "path/to/requirements.txt", "path/to/tmp"), fs.commands)
        self.assertIn(
            ("WRITE", "path/to/tmp/Dockerfile", "FROM TEST_BASE_IMAGE"), fs.commands
        )

    def test_build_image(self):
        docker_client = MagicMock()
        builder = DatackerBuilder(
            "test_image",
            [Path("hello_world_1.ipynb"), Path("hello_world_2.ipynb")],
            fs=FakeFileSystem(),
            docker_client=docker_client,
        )
        builder._build_image(working_path=Path("/tmp/test"))
        docker_client.images.build.assert_called_with(
            path="/tmp/test", tag="test_image"
        )

    def test_build(self):
        image_name = "datacker_test_create_image"
        notebooks = [Path("path/to/notebook.ipynb")]
        docker_client = MagicMock()
        fs = FakeFileSystem()
        builder = DatackerBuilder(
            image_name, notebooks, fs=fs, docker_client=docker_client
        )
        builder.build()
        self.assertIn(("TEMPORARY DIR", "fake/tmp/dir"), fs.commands)
        self.assertIn(("DELETE", "fake/tmp/dir"), fs.commands)
        self.assertIn(("COPY", "path/to/notebook.ipynb", "fake/tmp/dir"), fs.commands)
        docker_client.images.build.assert_called_with(
            path="fake/tmp/dir", tag=image_name
        )

    def test_build_with_dir(self):
        image_name = "datacker_test_create_image"
        notebooks = [Path("path/to/notebook.ipynb")]
        docker_client = MagicMock()
        fs = FakeFileSystem()
        builder = DatackerBuilder(
            image_name, notebooks, fs=fs, docker_client=docker_client
        )
        builder.build("/tmp/dir")
        self.assertNotIn(("TEMPORARY DIR", "fake/tmp/dir"), fs.commands)
        self.assertNotIn(("DELETE", "fake/tmp/dir"), fs.commands)
        self.assertIn(("COPY", "path/to/notebook.ipynb", "/tmp/dir"), fs.commands)
        docker_client.images.build.assert_called_with(path="/tmp/dir", tag=image_name)

    # def test_create_and_run_datacker(self):
    #     image_name = "datacker_test_create_image"
    #     notebooks = [
    #         Path(os.path.dirname(os.path.abspath(__file__)))
    #         / "notebooks"
    #         / "test.ipynb",
    #     ]
    #     builder = DatackerBuilder(image_name, notebooks)
    #     try:
    #         builder.build()

    #         docker_client.images.get(image_name)
    #         docker_client.containers.run(
    #             image_name, environment=dict(NOTEBOOK_NAME="test"),
    #         )
    #     finally:
    #         docker_client.images.remove(image_name, force=True)

    # def test_create_with_dir(self):
    #     image_name = "datacker_test_create_image"
    #     notebooks = [
    #         Path(os.path.dirname(os.path.abspath(__file__)))
    #         / "notebooks"
    #         / "test.ipynb",
    #     ]
    #     builder = DatackerBuilder(image_name, notebooks)
    #     try:
    #         with tempfile.TemporaryDirectory() as working_dir:
    #             builder.build(working_dir=working_dir)

    #         docker_client.images.get(image_name)
    #         docker_client.containers.run(
    #             image_name, environment=dict(NOTEBOOK_NAME="test"),
    #         )
    #     finally:
    #         docker_client.images.remove(image_name, force=True)
