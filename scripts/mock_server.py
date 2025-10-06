"""
Mock WebSocket backend for manual UI testing.

This server mimics the rasptank_controls websocket protocol enough for the
controller_web UI to be exercised locally without hardware.

Usage:
  python -m scripts.mock_server  # listens on 0.0.0.0:8889

In the UI, set Host to 127.0.0.1 and Port to 8889, then Connect.

Note: The `websockets` package is optional and not required for running tests.
This script guards the import so the rest of the repository (CI) isn't affected.
"""

from __future__ import annotations

import asyncio
import logging
from src.web_server import WebSocketHandler, success, failed

try:
    import websockets  # type: ignore
except Exception:  # pragma: no cover - optional dependency # pylint: disable=broad-exception-caught
    websockets = None  # pylint: disable=invalid-name


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(message)s")
LOGGER = logging.getLogger("mock_server")

SUPPORTED_COMMANDS = {
    # Movement
    "forward",
    "backward",
    "left",
    "right",
    "DS",
    "TS",
    # Servos
    "armUp",
    "armDown",
    "armStop",
    "handUp",
    "handDown",
    "handStop",
    "lookleft",
    "lookright",
    "LRstop",
    "grab",
    "loose",
    "GLstop",
    "up",
    "down",
    "UDstop",
    "home",
    # Info
    "get_info",
}

ARG_COMMANDS = {"wsB"}  # Commands requiring one integer argument

# Exported function for unit tests: takes a command string and returns a dict response


def command_handler(command_str: str):
    parts = command_str.split()
    cmd = parts[0] if parts else ""
    try:
        value = int(parts[1]) if len(parts) > 1 else None
    except Exception:  # pylint: disable=broad-exception-caught
        value = None

    if cmd in SUPPORTED_COMMANDS:
        LOGGER.info("Executed: %s", cmd)  # pylint: disable=logging-too-many-args
        return success(cmd, f"Command {cmd} Executed")
    if cmd in ARG_COMMANDS:
        if value is None:
            return failed(cmd, f"Command {cmd} Need 1 argument")
        LOGGER.info("Executed: %s, %s", cmd, value)  # pylint: disable=logging-too-many-args
        return success(cmd, f"Command {cmd} Executed")
    return failed(cmd, f"Command {cmd} Not Supported")


# Websocket handler for manual UI testing
ws_handler = WebSocketHandler(
    {s: (lambda s=s: LOGGER.info("Executed: %s", s)) for s in SUPPORTED_COMMANDS},  # pylint: disable=logging-too-many-args
    {
        s: (lambda s=s, value=None: LOGGER.info("Executed: %s, %s", s, value))  # pylint: disable=logging-too-many-args
        for s in ARG_COMMANDS
    },
)


async def _run(host: str = "0.0.0.0", port: int = 8889):  # pragma: no cover - network
    if websockets is None:
        raise RuntimeError(
            "The 'websockets' package is required to run the mock server. Install it via 'pip install websockets'."
        )
    LOGGER.info("Starting mock server on ws://%s:%d", host, port)  # pylint: disable=logging-too-many-args

    async with websockets.serve(ws_handler, host, port):
        await asyncio.Future()  # run forever


def run():  # pragma: no cover - convenience wrapper
    asyncio.run(_run())


if __name__ == "__main__":  # pragma: no cover
    run()
