import sys
import io
import unittest
from unittest.mock import patch, mock_open
from pathlib import Path

from ..run import get_config, get_parameters, run


class TestGetConfig(unittest.TestCase):
    def test_get_config_defaults(self):
        environment = {}
        expected = {
            "NOTEBOOK_NAME": "main",
            "NOTEBOOKS_PATH": Path("/notebooks"),
            "OUTPUT_PATH": Path("/output"),
            "OUTPUT_PREFIX": "%Y%m%d%H%M%S%f_",
            "OUTPUT_STDOUT": False,
        }
        result = get_config(environment)
        self.assertEqual(result, expected)

    def test_get_config(self):
        environment = {
            "NOTEBOOK_NAME": "test_notebook",
            "NOTEBOOKS_PATH": "/test_notebooks",
            "OUTPUT_PATH": "/test_output",
            "OUTPUT_PREFIX": "%Y%m%d_",
            "OUTPUT_STDOUT": "true",
        }
        expected = {
            "NOTEBOOK_NAME": "test_notebook",
            "NOTEBOOKS_PATH": Path("/test_notebooks"),
            "OUTPUT_PATH": Path("/test_output"),
            "OUTPUT_PREFIX": "%Y%m%d_",
            "OUTPUT_STDOUT": True,
        }
        result = get_config(environment)
        self.assertEqual(result, expected)


class TestGetParameters(unittest.TestCase):
    def test_get_json_param(self):
        environment = {"PARAMETERS": '{"var1": 3.1415, "var2": "Test value"}'}
        expected = {"var1": 3.1415, "var2": "Test value"}
        result = get_parameters(environment)
        self.assertEqual(result, expected)

    def test_get_param(self):
        environment = {"PARAM_var1": "3.1415", "PARAM_var2": '"Test value"'}
        expected = {"var1": 3.1415, "var2": "Test value"}
        result = get_parameters(environment)
        self.assertEqual(result, expected)

    def test_get_param_priority(self):
        environment = {
            "PARAMETERS": '{"var1": 3.1415, "var2": "Test value"}',
            "PARAM_var1": "3",
            "PARAM_var2": '"Another value"',
        }
        expected = {"var1": 3, "var2": "Another value"}
        result = get_parameters(environment)
        self.assertEqual(result, expected)


class TestRun(unittest.TestCase):
    @patch("datacker_runner.run.pm.execute_notebook")
    def test_run(self, mock_pm_execute_notebook):
        run(
            parameters={"param1": 1.1, "param2": "A string"},
            config={
                "NOTEBOOK_NAME": "test_notebook",
                "NOTEBOOKS_PATH": Path("/test_notebooks"),
                "OUTPUT_PATH": Path("/test_output"),
                "OUTPUT_PREFIX": "prefix_",
                "OUTPUT_STDOUT": False,
            },
        )
        mock_pm_execute_notebook.assert_called_with(
            Path("/test_notebooks/test_notebook.ipynb"),
            Path("/test_output/prefix_test_notebook.ipynb"),
            parameters={"param1": 1.1, "param2": "A string"},
        )

    @patch("datacker_runner.run.pm.execute_notebook")
    def test_output_stdout(self, mock_pm_execute_notebook):
        saved_stdout = sys.stdout
        try:
            output = io.StringIO()
            sys.stdout = output
            mock_open_notebook = mock_open(read_data="test_output")
            with patch("builtins.open", mock_open_notebook):
                run(
                    parameters={"param1": 1.1, "param2": "A string"},
                    config={
                        "NOTEBOOK_NAME": "test_notebook",
                        "NOTEBOOKS_PATH": Path("/test_notebooks"),
                        "OUTPUT_PATH": Path("/test_output"),
                        "OUTPUT_PREFIX": "prefix_",
                        "OUTPUT_STDOUT": True,
                    },
                )
            mock_open_notebook.assert_called_once_with(
                Path("/test_output/prefix_test_notebook.ipynb")
            )
            self.assertEqual(output.getvalue(), "test_output\n")
        finally:
            sys.stdout = saved_stdout
