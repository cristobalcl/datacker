import os
import unittest

import docker

from ..datacker import create_image, build_dockerfile, DOCKER_BASE


docker_client = docker.from_env()


class TestDockerfile(unittest.TestCase):
    def test_build_empty_dockerfile(self):
        expected = f"FROM {DOCKER_BASE}"
        dockerfile = build_dockerfile().split("\n")
        self.assertIn(expected, dockerfile)

    def test_add_one_notebook(self):
        expected = "ADD hello_world.ipynb /notebooks/"
        dockerfile = build_dockerfile(notebooks=("hello_world.ipynb",)).split("\n")
        self.assertIn(expected, dockerfile)

    # def test_remove_path_from_notebook(self):
    #     expected = "ADD hello_world.ipynb /notebooks/"
    #     dockerfile = build_dockerfile(notebooks=("path/to/hello_world.ipynb",)).split("\n")
    #     self.assertIn(expected, dockerfile)

    def test_add_many_notebook(self):
        expected = [
            "ADD hello_world_1.ipynb /notebooks/",
            "ADD hello_world_2.ipynb /notebooks/",
        ]
        dockerfile = build_dockerfile(
            notebooks=("hello_world_1.ipynb", "hello_world_2.ipynb")
        ).split("\n")
        for line in expected:
            self.assertIn(line, dockerfile)


class TestImage(unittest.TestCase):
    def test_create_image_from_notebook(self):
        image_name = "datacker_test_create_image"
        try:
            create_image(
                image_name,
                notebooks=[
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "notebooks",
                        "test.ipynb",
                    )
                ],
            )
            docker_client.images.get(image_name)
        finally:
            docker_client.images.remove(image_name, force=True)

    def test_run_image(self):
        image_name = "datacker_test_run_image"
        try:
            create_image(
                image_name,
                notebooks=[
                    os.path.join(
                        os.path.dirname(os.path.abspath(__file__)),
                        "notebooks",
                        "test.ipynb",
                    )
                ],
            )
            docker_client.containers.run(
                image_name,
                environment=dict(NOTEBOOK_NAME="test"),
                volumes={
                    "/output/": {"bind": "/home/cristobal/tmp/test", "mode": "rw"},
                },
            )
        finally:
            docker_client.images.remove(image_name, force=True)
