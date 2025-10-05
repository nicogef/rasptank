# tests/test_system.py
import json

import unittest
from unittest.mock import patch, mock_open, call
from src import system


def iterable_mock_open(read_data):
    mocked_open = mock_open(read_data=read_data)
    # Support: for line in f:
    mocked_open.return_value.__iter__.return_value = read_data.splitlines(True)
    return mocked_open


class TestSystemGetInfo(unittest.TestCase):

    @patch("builtins.open", new_callable=iterable_mock_open, read_data="45000\n")
    def test_get_info_returns_serializable_dict(self, mocked_open):
        # mocked_open = iterable_mock_open("45000\n")
        # with patch('builtins.open', mocked_open):
        info = system.get_info()
        expected_call = call("/sys/class/thermal/thermal_zone0/temp", "r", encoding='utf-8')
        self.assertIn(expected_call, mocked_open.call_args_list)

        self.assertIsInstance(info, list)
        # Keys should be strings
        self.assertTrue(all(isinstance(k, str) for k in info))
        # Entire payload should be JSON-serializable
        json.dumps(info, default=str)
