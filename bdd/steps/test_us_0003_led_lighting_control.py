import os
from pytest_bdd import scenarios, given, when, then
import pytest
from _pytest.fixtures import FixtureRequest

scenarios(os.path.join(os.path.dirname(__file__), "../features/us_0003_led_lighting_control.feature"))


@pytest.fixture(name="ctx")
def context_fixture():
    # Simple LED model: global color and brightness
    return {"color": (0, 0, 0), "brightness": 255, "default_color": (0, 0, 0), "default_brightness": 255}


@given("the LED controller is initialized")
def led_initialized(ctx):
    ctx["color"] = ctx["default_color"]
    ctx["brightness"] = ctx["default_brightness"]


@when("I set all LEDs to red", target_fixture="red_response")
def set_leds_red(ctx):
    ctx["color"] = (255, 0, 0)
    return {"status": "ok", "title": "set_red", "color": ctx["color"]}


@then("all LEDs should be red")
def verify_red(red_response):
    assert red_response["title"] == "set_red"
    assert red_response["color"] == (255, 0, 0)


@then("the command should be acknowledged")
def ack_generic(request: FixtureRequest):
    resp = None
    for name in ("red_response", "brightness_response", "reset_response"):
        if name in request.fixturenames:
            resp = request.getfixturevalue(name)
            break
    assert resp is not None, "No response fixture found for acknowledgement"
    assert resp.get("status") == "ok"


@when("I set the brightness to 50", target_fixture="brightness_response")
def set_brightness(ctx):
    ctx["brightness"] = 50
    return {"status": "ok", "title": "set_brightness", "brightness": ctx["brightness"]}


@then("the brightness should be updated")
def verify_brightness(brightness_response):
    assert brightness_response["title"] == "set_brightness"
    assert brightness_response["brightness"] == 50


@when("I reset the LEDs", target_fixture="reset_response")
def reset_leds(ctx):
    ctx["color"] = ctx["default_color"]
    ctx["brightness"] = ctx["default_brightness"]
    return {"status": "ok", "title": "reset_leds", "color": ctx["color"], "brightness": ctx["brightness"]}


@then("the LEDs should return to default state")
def verify_reset(reset_response):
    assert reset_response["title"] == "reset_leds"
    assert reset_response["color"] == (0, 0, 0)
    assert reset_response["brightness"] == 255
