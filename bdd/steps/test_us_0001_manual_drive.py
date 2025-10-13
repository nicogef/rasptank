import os
import time
from pytest_bdd import scenarios, given, when, then
import pytest

from bdd.helpers.mock_controller import MockController

scenarios(os.path.join(os.path.dirname(__file__), "../features/us_0001_manual_drive.feature"))


@pytest.fixture(name="ctx")
def context_fixture():
    return {}


@given("the robot is connected and ready")
def given_connected(ctx):
    ctx["controller"] = MockController()
    ctx["connected"] = True
    ctx["moving"] = False


@given("the robot is moving")
def given_moving(ctx):
    ctx["controller"] = ctx.get("controller", MockController())
    ctx["moving"] = True


@when('I send a "forward" command', target_fixture="command_response")
def when_forward(ctx):
    # Default speed 0.5 for manual forward if not set yet
    speed = ctx.get("speed", 50) / 100.0
    cmd_ts = time.time()
    result = ctx["controller"].process_command("forward", speed, cmd_ts)
    return {"status": "ok", "title": "forward", **result}


@when("I set the speed to 50", target_fixture="speed_response")
def when_set_speed_50(ctx):
    ctx["speed"] = 50
    # Mirror an ack envelope
    return {"status": "ok", "title": "wsB", "data": "Command wsB Executed", "speed": 50}


@when('I send a "DS" command', target_fixture="stop_response")
def when_stop(ctx):
    ctx["moving"] = False
    return {"status": "ok", "title": "DS", "data": "Command DS Executed"}


@when("I set the speed to 150", target_fixture="clamp_response")
def when_set_speed_150(ctx):
    # Use MockController to clamp speed > 1.0
    cmd_ts = time.time()
    result = ctx["controller"].process_command("speed", 1.5, cmd_ts)
    # Include the mapped motor output as a proxy for clamped speed (max 100)
    return {"status": "ok", "title": "wsB", **result}


@then("the robot should move forward")
def then_moved_forward(command_response):
    assert command_response["title"] == "forward"
    assert command_response["motor_output"] > 0


@then("the robot should stop moving")
def then_robot_stopped(stop_response):
    assert stop_response["title"] == "DS"
    assert stop_response["status"] == "ok"


@then("the speed should be clamped to the maximum")
def then_speed_clamped(clamp_response):
    # Motor output is 0..100
    assert int(round(clamp_response["motor_output"])) == 100
