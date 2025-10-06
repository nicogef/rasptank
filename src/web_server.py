"""
WebSocket protocol small helpers shared between rasptank_controls and mock_server.

This module is intentionally dependency-free so it can be imported in CI and
local environments without hardware or the websockets package present.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Callable


def success(title: str, data: Any) -> Dict[str, Any]:
    """Standard success envelope used by both backends."""
    return {"status": "ok", "title": title, "data": data}


def failed(title: str, data: Any) -> Dict[str, Any]:
    """Standard failure envelope used by both backends."""
    return {"status": "nok", "title": title, "data": data}


class WebSocketHandler:
    """Generic websocket handler that performs auth and dispatches messages.

    - check_permit: performs the credential handshake.
    - __call__: acts as the coroutine passed to websockets.serve.
    - process: shared generic message processing (list batching, JSON parsing).
    """

    def __init__(
        self,
        controls: Dict[str, Callable[[], None]] | None = None,
        controls_with_1_args: Dict[str, Callable[[Any], None]] | None = None,
        expected_user: str = "admin",
        expected_pass: str = "123456",
    ) -> None:
        self.expected_user = expected_user
        self.expected_pass = expected_pass
        self.controls = controls or {}
        self.controls_with_1_args = controls_with_1_args or {}

    async def check_permit(self, websocket) -> bool:
        """Simple credential handshake using username:password."""
        while True:
            recv_str = await websocket.recv()
            try:
                username, password = recv_str.split(":", 1)
            except ValueError:
                username, password = "", ""
            if username == self.expected_user and password == self.expected_pass:
                response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
                await websocket.send(response_str)
                return True
            await websocket.send("sorry, the username or password is wrong, please submit again")

    @staticmethod
    async def process(
        websocket,
        data: Any,
        controls_or_dispatch,
        controls_with_1_args: Dict[str, Callable[[Any], None]] | None = None,
    ):
        """Generic processing for a single received payload and send response(s).

        Compatibility:
        - If controls_or_dispatch is callable and controls_with_1_args is None, it is treated as a
          dispatch function taking a single str and returning a response dict.
        - Otherwise it is expected to be a controls dict and controls_with_1_args a dict of arg commands.
        """
        resp = None
        try:
            controls = controls_or_dispatch or {}
            arg_controls = controls_with_1_args or {}
            if isinstance(data, str):
                parts = data.split()
                cmd = parts[0]
                try:
                    value = int(parts[1]) if len(parts) > 1 else None
                except Exception:  # pylint: disable=broad-exception-caught
                    value = None
                if cmd in controls:
                    controls[cmd]()
                    resp = success(cmd, f"Command {cmd} Executed")
                elif cmd in arg_controls:
                    if value is not None:
                        arg_controls[cmd](value)
                        resp = success(cmd, f"Command {cmd} Executed")
                    else:
                        resp = failed(cmd, f"Command {cmd} Need 1 argument")
                else:
                    resp = failed(cmd, f"Command {cmd} Not Supported")
            else:
                resp = failed("unknown", f"Command Not Supported: {data}")
        finally:
            # Always send a response over the websocket
            await websocket.send(json.dumps(resp))

    async def __call__(self, websocket, _path=None):
        await self.check_permit(websocket)
        while True:
            raw = await websocket.recv()
            try:
                payload = json.loads(raw)
            except Exception:  # pylint: disable=broad-exception-caught
                payload = raw
            if payload is None or (isinstance(payload, str) and not payload.strip()):
                continue
            await self.process(websocket, payload, self.controls, self.controls_with_1_args)
