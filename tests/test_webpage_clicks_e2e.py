import os
import sys
import threading
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from contextlib import contextmanager

import pytest

# Ensure project root on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

playwright = pytest.importorskip("playwright.sync_api", reason="Playwright is required for E2E click test")
from playwright.sync_api import sync_playwright  # type: ignore  # noqa: E402  # pylint: disable=wrong-import-position
from scripts import mock_server  # pylint: disable=wrong-import-position


@contextmanager
def serve_controller_web():
    # Serve the project root so /controller_web is accessible
    root = os.path.dirname(os.path.dirname(__file__))
    cwd = os.getcwd()
    os.chdir(root)
    try:
        server = ThreadingHTTPServer(("127.0.0.1", 0), SimpleHTTPRequestHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{port}/controller_web/index.html"
        finally:
            server.shutdown()
            thread.join(timeout=3)
    finally:
        os.chdir(cwd)


def test_clicks_send_expected_commands():
    with serve_controller_web() as url:
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page()

            # Stub WebSocket in page to capture outbound messages produced by UI clicks
            page.add_init_script(
                r"""
                (function(){
                  const sent = [];
                  class WSStub {
                    static OPEN = 1;
                    static CLOSING = 2;
                    static CLOSED = 3;
                    constructor(url){
                      this.url = url;
                      this.readyState = WSStub.OPEN; // behave as open immediately
                      // Fire onopen asynchronously to mimic real behavior
                      setTimeout(() => { if (typeof this.onopen === 'function') this.onopen(); }, 0);
                    }
                    send(msg){ sent.push(String(msg)); }
                    close(){ this.readyState = WSStub.CLOSED; if (typeof this.onclose === 'function') this.onclose(); }
                  }
                  window.__sent_ws_msgs__ = sent;
                  window.WebSocket = WSStub;
                })();
                """
            )

            page.goto(url)

            # Fill connection fields just to satisfy UI, then click Connect (uses stub)
            page.fill("#host", "127.0.0.1")
            page.fill("#port", "8889")
            page.fill("#username", "admin")
            page.fill("#password", "123456")
            page.click("#btnConnect")

            # Click all data-cmd buttons
            buttons = page.query_selector_all("[data-cmd]")
            assert buttons, "No command buttons found on the page"
            for btn in buttons:
                btn.click()

            # Click Get Info and Set Speed too
            page.click("#btnGetInfo")
            page.fill("#speed", "42")  # set value, then click Set Speed
            page.click("#btnSetSpeed")

            # Read captured messages
            sent = page.evaluate("window.__sent_ws_msgs__")
            browser.close()

    # After clicking, the first message should be the credential handshake
    assert any(m.startswith("admin:") for m in sent), f"Handshake not sent: {sent}"

    # Extract commands that were sent by clicks (ignore handshake)
    clicked_cmds = [m for m in sent if not m.startswith("admin:")]
    assert clicked_cmds, "No commands were sent by clicking buttons"

    # Validate that every message either matches a no-arg supported command or is a wsB <num>
    sup = set(mock_server.SUPPORTED_COMMANDS)
    for m in clicked_cmds:
        parts = m.split()
        cmd = parts[0]
        if cmd in sup:
            continue
        if cmd == "wsB":
            assert len(parts) == 2 and parts[1].isdigit(), f"wsB should have a numeric arg: {m}"
            continue
        pytest.fail(f"Unexpected command sent by UI: {m}")
