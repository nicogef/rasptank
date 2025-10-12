from pytest_bdd import scenarios, given, when, then
import os
import pytest

scenarios(os.path.join(os.path.dirname(__file__), '../features/us_0002_gimbal_servo_control.feature'))

@pytest.fixture
def ctx():
    # simple servo model
    return {"angle": 90, "min": 0, "max": 180}

@given('the camera servo is initialized')
def servo_initialized(ctx):
    ctx["angle"] = 90

@when('I send an "up" command', target_fixture='up_response')
def send_up(ctx):
    # simulate moving up towards max
    ctx["angle"] = min(ctx["max"], ctx["angle"] + 10)
    return {"status": "ok", "title": "up", "angle": ctx["angle"]}

@then('the camera should move up')
def camera_moves_up(up_response):
    assert up_response["title"] == "up"
    assert up_response["angle"] >= 90

@when('I send a "home" command', target_fixture='home_response')
def send_home(ctx):
    ctx["angle"] = 90
    return {"status": "ok", "title": "home", "angle": ctx["angle"]}

@then('the camera should return to center position')
def camera_center(home_response):
    assert home_response["title"] == "home"
    assert home_response["angle"] == 90

@when('I move the camera to angle 90', target_fixture='angle_response')
def move_to_90(ctx):
    ctx["angle"] = 90
    return {"status": "ok", "title": "move_to_angle", "angle": ctx["angle"]}

@then('the camera should be at angle 90')
def verify_at_90(angle_response):
    assert angle_response["title"] == "move_to_angle"
    assert angle_response["angle"] == 90
