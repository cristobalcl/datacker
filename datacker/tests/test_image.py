import os
import unittest
from pathlib import Path

import docker

from ..fs import FileSystemInterface
from ..images import build_dockerfile, build_directory, DOCKER_BASE
from .. import build_datacker


docker_client = docker.from_env()


class TestDockerfile(unittest.TestCase):
    def test_build_empty_dockerfile(self):
        expected = f"FROM {DOCKER_BASE}"
        dockerfile = build_dockerfile([]).split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_one_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        dockerfile = build_dockerfile(notebooks=[Path("hello_world.ipynb")]).split("\n")
        self.assertIn(expected, dockerfile)

    def test_remove_path_from_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        dockerfile = build_dockerfile(
            notebooks=[Path("path/to/hello_world.ipynb")],
        ).split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_many_notebook(self):
        expected = [
            "ADD hello_world_1.ipynb /notebooks/",
            "ADD hello_world_2.ipynb /notebooks/",
        ]
        dockerfile = build_dockerfile(
            notebooks=[Path("hello_world_1.ipynb"), Path("hello_world_2.ipynb")]
        ).split("\n")
        for line in expected:
            self.assertIn(line, dockerfile)


class FakeFileSystem(FileSystemInterface):
    def __init__(self):
        self.commands = []

    def write(self, filename: Path, content: str):
        self.commands.append(("WRITE", str(filename), content))

    def copy(self, source: Path, dest: Path):
        self.commands.append(("COPY", str(source), str(dest)))


class TestSetupDirectory(unittest.TestCase):
    def test_build_directory(self):
        fs = FakeFileSystem()
        build_directory(
            notebooks=[Path("notebook_1.ipynb"), Path("notebook_2.ipynb")],
            dockerfile="FROM TEST_BASE_IMAGE",
            working_dir=Path("path/to/tmp"),
            fs=fs,
        )
        self.assertIn(("COPY", "notebook_1.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(("COPY", "notebook_2.ipynb", "path/to/tmp"), fs.commands)
        self.assertIn(
            ("WRITE", "path/to/tmp/Dockerfile", "FROM TEST_BASE_IMAGE"), fs.commands
        )


class TestBuildDatacker(unittest.TestCase):
    def test_create_run_datacker(self):
        image_name = "datacker_test_create_image"
        notebooks = [
            Path(os.path.dirname(os.path.abspath(__file__)))
            / "notebooks"
            / "test.ipynb",
        ]
        try:
            build_datacker(image_name, notebooks)

            docker_client.images.get(image_name)
            docker_client.containers.run(
                image_name, environment=dict(NOTEBOOK_NAME="test"),
            )
        finally:
            docker_client.images.remove(image_name, force=True)


#     def test_run_image(self):
#         image_name = "datacker_test_run_image"
#         try:
#             create_image(
#                 image_name,
#                 notebooks=[
#                     os.path.join(
#                         os.path.dirname(os.path.abspath(__file__)),
#                         "notebooks",
#                         "test.ipynb",
#                     )
#                 ],
#             )
#             docker_client.containers.run(
#                 image_name,
#                 environment=dict(NOTEBOOK_NAME="test"),
#                 # volumes={
#                 #     "/output/": {"bind": "/home/cristobal/tmp/test", "mode": "rw"},
#                 # },
#             )
#         finally:
#             docker_client.images.remove(image_name, force=True)
