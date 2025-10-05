# tests/test_system.py
import json

import unittest
from unittest.mock import patch, mock_open, call
from src import system

def iterable_mock_open(read_data):
    m = mock_open(read_data=read_data)
    # Support: for line in f:
    m.return_value.__iter__.return_value = read_data.splitlines(True)
    return m

class TestSystemGetInfo(unittest.TestCase):

    @patch('builtins.open', new_callable=iterable_mock_open, read_data="45000\n")
    def test_get_info_returns_serializable_dict(self, m):
        # m = iterable_mock_open("45000\n")
        # with patch('builtins.open', m):
        info = system.get_info()
        expected_call = call("/sys/class/thermal/thermal_zone0/temp", "r")
        self.assertIn(expected_call, m.call_args_list)

        self.assertIsInstance(info, list)
        # Keys should be strings
        self.assertTrue(all(isinstance(k, str) for k in info))
        # Entire payload should be JSON-serializable
        json.dumps(info, default=str)
