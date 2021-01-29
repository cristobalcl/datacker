import unittest

from ..run import get_parameters


class TestGetParameters(unittest.TestCase):
    def test_get_json_param(self):
        parameters = {"PARAMETERS": '{"var1": 3.1415, "var2": "Test value"}'}
        expected = {"var1": 3.1415, "var2": "Test value"}
        result = get_parameters(parameters)
        self.assertEqual(result, expected)

    def test_get_param(self):
        parameters = {"PARAM_var1": "3.1415", "PARAM_var2": '"Test value"'}
        expected = {"var1": 3.1415, "var2": "Test value"}
        result = get_parameters(parameters)
        self.assertEqual(result, expected)

    def test_get_param_priority(self):
        parameters = {
            "PARAMETERS": '{"var1": 3.1415, "var2": "Test value"}',
            "PARAM_var1": "3",
            "PARAM_var2": '"Another value"',
        }
        expected = {"var1": 3, "var2": "Another value"}
        result = get_parameters(parameters)
        self.assertEqual(result, expected)
