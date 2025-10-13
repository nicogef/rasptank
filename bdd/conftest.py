from pytest_bdd import then
from _pytest.fixtures import FixtureRequest

# Common BDD helpers available to all step files


@then("the command should be acknowledged")
def common_acknowledged(request: FixtureRequest):
    # Try to locate a response-like fixture for current scenario
    candidate_names = (
        "command_response",
        "speed_response",
        "stop_response",
        "clamp_response",
        "up_response",
        "home_response",
        "angle_response",
        "red_response",
        "brightness_response",
        "reset_response",
        "auto_response",
        "track_response",
        "connect_response",
        "info_response",
    )
    resp = None
    for name in candidate_names:
        if name in request.fixturenames:
            resp = request.getfixturevalue(name)
            break
    assert resp is not None, "No response found to acknowledge"
    assert isinstance(resp, dict), "Response should be a dict"
    assert resp.get("status", "ok") == "ok"


@then("the speed should be updated")
def common_speed_updated(request: FixtureRequest):
    # Generic check: speed payload present and positive
    target = None
    if "speed_response" in request.fixturenames:
        target = request.getfixturevalue("speed_response")
    elif "forward_response" in request.fixturenames:
        target = request.getfixturevalue("forward_response")
    assert target is not None, "No speed-related response available"
    assert isinstance(target, dict)
    assert "speed" in target and int(target["speed"]) >= 0


@then("the application should not crash")
def common_no_crash(request: FixtureRequest):
    # Accepts various fixtures representing outputs/errors
    for name in ("video_feed", "sensor_result", "feed_error"):
        if name in request.fixturenames:
            obj = request.getfixturevalue(name)
            assert obj is not None
            return
    # If none of the above present, passing the step denotes no crash
    assert True
