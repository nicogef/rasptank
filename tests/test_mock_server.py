import unittest
from scripts import mock_server


class TestMockServerDispatch(unittest.TestCase):
    def test_success_no_arg(self):
        resp = mock_server.command_handler("forward")
        self.assertEqual(resp["status"], "ok")
        self.assertEqual(resp["title"], "forward")

    def test_success_with_arg(self):
        resp = mock_server.command_handler("wsB 42")
        self.assertEqual(resp["status"], "ok")
        self.assertEqual(resp["title"], "wsB")

    def test_missing_arg(self):
        resp = mock_server.command_handler("wsB")
        self.assertEqual(resp["status"], "nok")
        self.assertIn("Need 1 argument", resp["data"])

    def test_unsupported(self):
        resp = mock_server.command_handler("unknown")
        self.assertEqual(resp["status"], "nok")
        self.assertIn("Not Supported", resp["data"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
