import os
import re
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from scripts import mock_server  # pylint: disable=wrong-import-position


class TestWebpageActionsAgainstMock(unittest.TestCase):
    def setUp(self):
        # Load the standalone controller UI HTML
        root = os.path.dirname(os.path.dirname(__file__))
        html_path = os.path.join(root, "controller_web", "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            self.html = f.read()

    def test_buttons_are_supported_by_mock(self):
        # Extract all data-cmd attributes declared in the UI
        cmds = set(re.findall(r'data-cmd="([^"]+)"', self.html))
        # Verify every UI action without args is supported by the mock backend
        unsupported = cmds - set(mock_server.SUPPORTED_COMMANDS)
        self.assertFalse(
            unsupported,
            msg=f"Unsupported commands in mock_server.SUPPORTED_COMMANDS: {sorted(unsupported)}",
        )

    def test_speed_and_info_actions(self):
        # wsB must be supported as an argumented command in the mock
        self.assertIn("wsB", mock_server.ARG_COMMANDS)
        # The page exposes an Info button; ensure mock supports get_info
        self.assertIn("get_info", mock_server.SUPPORTED_COMMANDS)

    def test_command_handler_contract(self):
        # For each UI command (no-arg), the mock handler should return ok
        cmds = set(re.findall(r'data-cmd="([^"]+)"', self.html))
        for cmd in cmds:
            if cmd in mock_server.SUPPORTED_COMMANDS:
                resp = mock_server.command_handler(cmd)
                self.assertEqual(resp.get("status"), "ok", msg=f"{cmd} should be ok")
                self.assertEqual(resp.get("title"), cmd)

        # For speed (wsB), missing arg => nok, with arg => ok
        resp = mock_server.command_handler("wsB")
        self.assertEqual(resp.get("status"), "nok")
        self.assertIn("Need 1 argument", resp.get("data", ""))

        for val in (0, 50, 100):
            resp = mock_server.command_handler(f"wsB {val}")
            self.assertEqual(resp.get("status"), "ok")
            self.assertEqual(resp.get("title"), "wsB")


if __name__ == "__main__":
    unittest.main(verbosity=2)
