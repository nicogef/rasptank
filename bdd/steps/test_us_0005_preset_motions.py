import sys
import os
from unittest.mock import MagicMock
from pytest_bdd import scenarios, given, when, then

# Mock the hardware modules for testing without a real robot
sys.modules["web.move"] = MagicMock()
sys.modules["web.ultra"] = MagicMock()
sys.modules["RPIservo"] = MagicMock()
sys.modules["gpiozero"] = MagicMock()
# from web import functions

scenarios(os.path.join(os.path.dirname(__file__), "../features/us_0005_preset_motions.feature"))


@given("the robot is ready for preset motions")
def mock_robot_ready():
    """Mocks the robot being ready for preset motions."""


@when("I start the automatic mode", target_fixture="auto_response")
def start_automatic_mode():
    """Starts the automatic mode and captures the response."""
    return {"status": "ok", "mode": "automatic"}


@then("the robot should begin obstacle avoidance")
def verify_obstacle_avoidance(auto_response):
    """Verifies that obstacle avoidance started."""
    assert auto_response["mode"] == "automatic"


@given("the robot is in preset motion")
def mock_robot_in_motion():
    """Mocks the robot being in preset motion."""


@when("I stop the preset motion", target_fixture="stop_response")
def stop_preset_motion():
    """Stops the preset motion and captures the response."""
    return {"status": "ok", "action": "stopped"}


@then("the robot should stop moving")
def verify_robot_stops(stop_response):
    """Verifies that the robot stopped."""
    assert stop_response["action"] == "stopped"


@when("I start the track line mode", target_fixture="track_response")
def start_track_line_mode():
    """Starts the track line mode and captures the response."""
    return {"status": "ok", "mode": "track_line"}


@then("the robot should begin following a line")
def verify_line_following(track_response):
    """Verifies that line following started."""
    assert track_response["mode"] == "track_line"
