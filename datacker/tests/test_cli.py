import unittest
from unittest.mock import patch, MagicMock

from typer.testing import CliRunner

from ..cli import app


runner = CliRunner()


class TestCLI(unittest.TestCase):
    @patch("datacker.cli.DatackerBuilder")
    def test_cli(self, MockDatackerBuilder):
        mock_build = MagicMock()
        MockDatackerBuilder.return_value = mock_build
        runner.invoke(
            app,
            [
                "test_image",
                "notebook1.ipynb",
                "notebook2.ipynb",
                "notebook3.ipynb",
                "-r",
                "path/to/requirements.txt",
            ],
        )
        MockDatackerBuilder.assert_called_with(
            "test_image",
            ["notebook1.ipynb", "notebook2.ipynb", "notebook3.ipynb"],
            requirements_file="path/to/requirements.txt",
        )
        mock_build.build.assert_called()
