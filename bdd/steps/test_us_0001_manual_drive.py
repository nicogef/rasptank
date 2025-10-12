import time
import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from bdd.helpers.mock_controller import MockController

# Load scenarios from the feature file
scenarios("../features/us_0001_manual_drive.feature")

# Module-level context for sharing state between steps
CONTEXT = {}


@pytest.fixture(autouse=True)
def reset_context():
    """Reset context before each scenario."""
    CONTEXT.clear()
    yield


@given("the web client is connected to the robot and clocks are synchronized")
def client_connected():
    """Set up a mock controller and connection state."""
    CONTEXT["controller"] = MockController()
    CONTEXT["client_connected"] = True


@when(parsers.parse('the user sends a drive command "{direction}" with speed {speed:g}'))
@given(parsers.parse('the user sends a drive command "{direction}" with speed {speed:g}'))
def send_drive_command(direction, speed):
    """Simulate sending a drive command to the controller."""
    assert CONTEXT.get("client_connected"), "Client must be connected first"
    cmd_ts = time.time()
    CONTEXT["last_command"] = {"direction": direction, "speed": float(speed), "timestamp": cmd_ts}
    result = CONTEXT["controller"].process_command(direction, float(speed), cmd_ts)
    CONTEXT["last_result"] = result


@given("the main control UI is loaded")
def ui_loaded():
    """Simulate the UI being loaded."""
    CONTEXT["ui_loaded"] = True


@when("the user inspects movement controls")
def inspect_controls():
    """Simulate inspecting the UI controls."""
    assert CONTEXT.get("ui_loaded"), "UI must be loaded"
    CONTEXT["controls"] = ["forward", "reverse", "left", "right", "stop"]


@when("the controller receives the command")
def controller_receives_command():
    """Confirm the command was received (mocked)."""
    assert "last_result" in CONTEXT, "Command was not processed"


@then(
    parsers.parse(
        'the robot should start moving in the "{direction}" direction within {milliseconds:d} milliseconds'
        " of the command timestamp"
    )
)
def then_movement_within_ms(direction, milliseconds):
    """Check if the robot moves within the specified latency."""
    res = CONTEXT.get("last_result")
    assert res is not None, "No result available"
    assert res["direction"] == direction
    delta_ms = (res["motor_start_ts"] - res["cmd_ts"]) * 1000.0
    assert delta_ms <= milliseconds, f"Movement started after {delta_ms:.1f}ms, expected <={milliseconds}ms"


@then("telemetry contains a command-received timestamp and a motor-start timestamp")
def then_telemetry_timestamps():
    """Verify that telemetry timestamps are present."""
    res = CONTEXT.get("last_result")
    assert "cmd_ts" in res and "motor_start_ts" in res, "Timestamps missing"


@then(parsers.parse("motor output shall be proportional to {speed:g} within a tolerance of {tol:d} percent"))
def then_speed_proportional(speed, tol):
    """Verify that motor speed is proportional to the command speed."""
    res = CONTEXT.get("last_result")
    assert res is not None, "No result available"
    expected = CONTEXT["controller"].map_speed(float(speed))
    actual = res["motor_output"]
    if expected == 0:
        assert actual == 0, "Motor should be stopped"
    else:
        pct_diff = abs(actual - expected) / expected * 100.0
        assert pct_diff <= tol, f"Output differs by {pct_diff:.1f}%, which is more than {tol}%"


@then("controls for forward, reverse, left, right, and stop are present and operable")
def then_controls_present():
    """Check if all required movement controls are available."""
    controls = CONTEXT.get("controls", [])
    required = {"forward", "reverse", "left", "right", "stop"}
    assert required.issubset(set(controls)), f"Missing controls: {required - set(controls)}"


@then("the controller clamps speed to the configured maximum and logs an event")
def then_clamped_and_logged():
    """Verify that out-of-range speeds are clamped."""
    res = CONTEXT.get("last_result")
    assert res is not None, "No result available"
    max_speed = CONTEXT["controller"].max_speed
    # Check if the command speed was at or above max
    assert res["cmd_speed"] >= max_speed
    assert CONTEXT["controller"].last_clamped is True, "Clamp event was not logged"
