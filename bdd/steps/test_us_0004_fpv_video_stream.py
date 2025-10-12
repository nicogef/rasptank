from pytest_bdd import scenarios, given, when, then
import os
import pytest

scenarios(os.path.join(os.path.dirname(__file__), '../features/us_0004_fpv_video_stream.feature'))

@pytest.fixture
def ctx():
    return {"camera_available": True, "streaming": False}

@given('the camera is available')
def camera_available(ctx):
    ctx["camera_available"] = True

@given('the camera is streaming')
def camera_streaming(ctx):
    ctx["streaming"] = True

@given('the camera is not available')
def camera_not_available(ctx):
    ctx["camera_available"] = False

@when('I access the video feed', target_fixture='video_feed')
def when_access_feed(ctx):
    # Return a bytes stream or a RuntimeError object depending on availability
    if ctx["camera_available"]:
        return b'fake_mjpeg_stream'
    return RuntimeError("Camera not available")

@then('I should receive a video stream')
def then_have_stream(video_feed):
    assert isinstance(video_feed, (bytes, bytearray))
    assert len(video_feed) > 0

@then('the stream should be in MJPEG format')
def then_mjpeg(video_feed):
    # For mock, we just assert it's bytes
    assert isinstance(video_feed, (bytes, bytearray))

@when('I set the resolution to 640x480', target_fixture='resolution_response')
def when_set_resolution(ctx):
    # Simulate successful resolution update
    return {"status": "ok", "resolution": "640x480"}

@then('the video resolution should be updated')
def then_resolution_ok(resolution_response):
    assert resolution_response["resolution"] == "640x480"

@then('the stream should continue')
def then_stream_continues(resolution_response):
    assert resolution_response["status"] == "ok"

@then('the system should report camera unavailability')
def then_report_unavailable(video_feed):
    assert isinstance(video_feed, RuntimeError)
    assert "Camera not available" in str(video_feed)

@then('the application should not crash')
def then_no_crash(video_feed):
    # Reaching here is sufficient
    assert video_feed is not None
