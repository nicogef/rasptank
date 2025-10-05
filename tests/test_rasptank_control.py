# python
import unittest
from unittest.mock import Mock, AsyncMock, patch
import sys
import os
import json
import asyncio

# Ensure project root on path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Mock hardware dependencies BEFORE importing module
sys.modules["src.hardware.pca9685_controller"] = Mock()
sys.modules["src.hardware.spi_controller"] = Mock()
sys.modules["src.controllers.servo"] = Mock()
sys.modules["src.controllers.motors"] = Mock()
sys.modules["src.controllers.leds"] = Mock()
# sys.modules['src.system'] = Mock()
sys.modules["app"] = Mock()
sys.modules["websockets"] = Mock()

from src import rasptank_controls  # pylint: disable=wrong-import-position


def rebind_movement(mock_movement):
    rasptank_controls.MOVEMENT = mock_movement
    rasptank_controls.controls.update(
        {
            "forward": mock_movement.forward,
            "backward": mock_movement.backward,
            "left": mock_movement.left,
            "right": mock_movement.right,
            "DS": mock_movement.stop,
            "TS": mock_movement.stop,
        }
    )
    rasptank_controls.controls_with_1_args.update({"wsB": mock_movement.set_speed})


def rebind_servos(arm, hand, wrist, claw, cam):
    rasptank_controls.ARM = arm
    rasptank_controls.HAND = hand
    rasptank_controls.WRIST = wrist
    rasptank_controls.CLAW = claw
    rasptank_controls.CAMERA = cam
    rasptank_controls.controls.update(
        {
            "armUp": arm.clockwise,
            "armDown": arm.anticlockwise,
            "armStop": arm.stop,
            "handUp": hand.clockwise,
            "handDown": hand.anticlockwise,
            "handStop": hand.stop,
            "lookleft": wrist.clockwise,
            "lookright": wrist.anticlockwise,
            "LRstop": wrist.stop,
            "grab": claw.clockwise,
            "loose": claw.anticlockwise,
            "GLstop": claw.stop,
            "up": cam.clockwise,
            "down": cam.anticlockwise,
            "UDstop": cam.stop,
            "home": rasptank_controls.servoPosInit,
        }
    )


class TestResponses(unittest.TestCase):
    def test_success(self):
        self.assertEqual(
            rasptank_controls.success("cmd", 123),
            {"status": "ok", "title": "cmd", "data": 123},
        )

    def test_failed(self):
        self.assertEqual(
            rasptank_controls.failed("cmd", "err"),
            {"status": "nok", "title": "cmd", "data": "err"},
        )


class TestServoInit(unittest.TestCase):
    def test_servo_pos_init(self):
        arm = Mock()
        hand = Mock()
        wrist = Mock()
        claw = Mock()
        cam = Mock()
        rebind_servos(arm, hand, wrist, claw, cam)
        rasptank_controls.servoPosInit()
        arm.reset.assert_called_once()
        hand.reset.assert_called_once()
        wrist.reset.assert_called_once()
        cam.reset.assert_called_once()
        claw.reset.assert_called_once()


class TestServoControls(unittest.TestCase):
    def setUp(self):
        self.arm = Mock()
        self.hand = Mock()
        self.wrist = Mock()
        self.claw = Mock()
        self.cam = Mock()
        rebind_servos(self.arm, self.hand, self.wrist, self.claw, self.cam)

    def test_arm_controls(self):
        rasptank_controls.controls["armUp"]()
        self.arm.clockwise.assert_called_once()
        rasptank_controls.controls["armDown"]()
        self.arm.anticlockwise.assert_called_once()
        rasptank_controls.controls["armStop"]()
        self.arm.stop.assert_called_once()

    def test_wrist_controls(self):
        rasptank_controls.controls["lookleft"]()
        self.wrist.clockwise.assert_called_once()
        rasptank_controls.controls["lookright"]()
        self.wrist.anticlockwise.assert_called_once()
        rasptank_controls.controls["LRstop"]()
        self.wrist.stop.assert_called_once()


class TestMovementControls(unittest.TestCase):
    def setUp(self):
        self.movement = Mock()
        rebind_movement(self.movement)

    def test_moves(self):
        rasptank_controls.controls["forward"]()
        self.movement.forward.assert_called_once()
        rasptank_controls.controls["backward"]()
        self.movement.backward.assert_called_once()
        rasptank_controls.controls["left"]()
        self.movement.left.assert_called_once()
        rasptank_controls.controls["right"]()
        self.movement.right.assert_called_once()

    def test_stops(self):
        rasptank_controls.controls["DS"]()
        self.movement.stop.assert_called_once()
        rasptank_controls.controls["TS"]()
        self.assertEqual(self.movement.stop.call_count, 2)

    def test_set_speed_arg_command(self):
        rasptank_controls.controls_with_1_args["wsB"](60)
        self.movement.set_speed.assert_called_once_with(60)


class TestWifiCheck(unittest.TestCase):
    def test_wifi_check_no_socket_import(self):
        # Inject mock socket (module lacks import)
        mock_socket_mod = Mock()
        mock_sock = Mock()
        mock_sock.getsockname.return_value = ["10.0.0.2"]
        mock_socket_mod.socket.return_value = mock_sock
        rasptank_controls.socket = mock_socket_mod
        rasptank_controls.wifi_check()
        mock_socket_mod.socket.assert_called_once()


class TestGetInfo(unittest.TestCase):
    def setUp(self):
        # Patch system.get_info then rebind controls entry
        self.get_info_mock = Mock(return_value={"version": "1.0", "ok": True})
        rasptank_controls.system.get_info = self.get_info_mock
        rasptank_controls.controls["get_info"] = rasptank_controls.system.get_info

    def test_get_info_control_mapping(self):
        result = rasptank_controls.controls["get_info"]()
        self.get_info_mock.assert_called_once()
        self.assertEqual(result, {"version": "1.0", "ok": True})


class TestAsyncFlow(unittest.IsolatedAsyncioTestCase):
    async def test_check_permit_valid(self):
        ws = AsyncMock()
        ws.recv.return_value = "admin:123456"
        ok = await rasptank_controls.check_permit(ws)
        self.assertTrue(ok)
        ws.send.assert_called_once()
        self.assertIn("congratulation", ws.send.call_args[0][0])

    async def test_check_permit_retry(self):
        ws = AsyncMock()
        ws.recv.side_effect = ["user:bad", "admin:123456"]
        ok = await rasptank_controls.check_permit(ws)
        self.assertTrue(ok)
        self.assertEqual(ws.send.call_count, 2)

    async def test_recv_msg_forward(self):
        ws = AsyncMock()
        ws.recv.side_effect = ["forward", asyncio.CancelledError()]
        movement = Mock()
        rebind_movement(movement)
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        movement.forward.assert_called_once()
        sent = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(sent["title"], "forward")
        self.assertEqual(sent["status"], "ok")

    async def test_recv_msg_invalid(self):
        ws = AsyncMock()
        ws.recv.side_effect = ["foo", asyncio.CancelledError()]
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        sent = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(sent["status"], "nok")

    async def test_recv_msg_missing_arg(self):
        ws = AsyncMock()
        ws.recv.side_effect = ["wsB", asyncio.CancelledError()]
        movement = Mock()
        rebind_movement(movement)
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        sent = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(sent["status"], "nok")
        self.assertIn("Need 1 argument", sent["data"])

    async def test_recv_msg_get_info(self):
        # Prepare websocket returning the command then raising to exit loop
        ws = AsyncMock()
        ws.recv.side_effect = ["get_info", asyncio.CancelledError()]
        # Patch and rebind get_info
        get_info_mock = Mock(return_value={"cpu": "pct"})
        rasptank_controls.system.get_info = get_info_mock
        rasptank_controls.controls["get_info"] = rasptank_controls.system.get_info
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        get_info_mock.assert_called_once()
        sent_payload = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(sent_payload["status"], "ok")
        self.assertEqual(sent_payload["title"], "get_info")
        self.assertIn("Executed", sent_payload["data"])


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestAdditionalAsyncFlows(unittest.IsolatedAsyncioTestCase):
    async def test_recv_msg_one_arg_success(self):
        # Ensure movement is rebound and callable via command router
        movement = Mock()
        rebind_movement(movement)
        ws = AsyncMock()
        # Provide a command with an integer argument
        ws.recv.side_effect = ["wsB 75", asyncio.CancelledError()]
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        # Should have called set_speed with 75 and sent an ok response
        movement.set_speed.assert_called_once_with(75)
        payload = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["title"], "wsB")

    async def test_recv_msg_non_string_payload(self):
        ws = AsyncMock()
        # Send JSON object so that json.loads yields a dict (non-str)
        ws.recv.side_effect = ["{}", asyncio.CancelledError()]
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        payload = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(payload["status"], "nok")
        self.assertEqual(payload["title"], "unknown")

    async def test_recv_msg_home_calls_servo_init(self):
        # Mock servos and ensure servoPosInit is invoked through command router
        arm = Mock()
        hand = Mock()
        wrist = Mock()
        claw = Mock()
        cam = Mock()
        rebind_servos(arm, hand, wrist, claw, cam)
        ws = AsyncMock()
        ws.recv.side_effect = ["home", asyncio.CancelledError()]
        with self.assertRaises(asyncio.CancelledError):
            await rasptank_controls.recv_msg(ws)
        # servoPosInit should have been called, which triggers reset on each servo
        arm.reset.assert_called_once()
        hand.reset.assert_called_once()
        wrist.reset.assert_called_once()
        claw.reset.assert_called_once()
        cam.reset.assert_called_once()
        payload = json.loads(ws.send.call_args_list[0].args[0])
        self.assertEqual(payload["status"], "ok")
        self.assertEqual(payload["title"], "home")


class TestWifiCheckAPBranch(unittest.TestCase):
    def test_wifi_check_triggers_ap_on_exception(self):
        # Force socket creation to raise to hit AP thread branch
        rasptank_controls.socket = Mock()
        rasptank_controls.socket.socket.side_effect = Exception("no network")
        # Replace ap_thread with a mock so we don't run os.system
        rasptank_controls.ap_thread = Mock()

        # Patch threading.Thread to a dummy that records calls
        class DummyThread:
            def __init__(
                self, *args, target=None, **kwargs
            ):  # pylint: disable=unused-argument
                self.target = target
                self.daemon = False
                self.started = False

            def start(self):
                # do not invoke target to avoid side effects
                self.started = True

        with patch.object(rasptank_controls, "threading", Mock(Thread=DummyThread)):
            rasptank_controls.wifi_check()
            # ap_thread should not have been executed, only scheduled
            self.assertFalse(rasptank_controls.ap_thread.called)
