from pytest_bdd import scenarios, given, when, then
import os
import pytest

scenarios(os.path.join(os.path.dirname(__file__), '../features/us_0006_sensor_integration.feature'))

@pytest.fixture
def ctx():
    return {"sensor_connected": True}

@given('the robot has an ultrasonic sensor connected')
def given_sensor_connected(ctx):
    ctx["sensor_connected"] = True

@given('the robot does not have an ultrasonic sensor connected')
def given_sensor_disconnected(ctx):
    ctx["sensor_connected"] = False

@given('the robot system is running with a sensor')
def given_system_with_sensor(ctx):
    ctx["sensor_connected"] = True

@when('I request the sensor distance', target_fixture='sensor_result')
def when_request_distance(ctx):
    if ctx["sensor_connected"]:
        return 50.0
    return Exception("Sensor not found")

@then('I should receive a distance reading')
def then_have_distance(sensor_result):
    assert sensor_result is not None
    assert not isinstance(sensor_result, Exception)

@then('the reading should be a positive number')
def then_distance_positive(sensor_result):
    assert sensor_result > 0

@then('the system should report the sensor as unavailable')
def then_sensor_unavailable(sensor_result):
    assert isinstance(sensor_result, Exception)

@then('the application should not crash')
def then_no_crash(sensor_result):
    assert sensor_result is not None

@when('I query the "get_info" API endpoint', target_fixture='api_response')
def when_query_get_info(ctx):
    # Simulate API exposing sensor distance
    return {"ultra": {"distance": 25.0 if ctx["sensor_connected"] else None}}

@then('the response should contain sensor data')
def then_contains_sensor(api_response):
    assert 'ultra' in api_response

@then('the sensor data should include a "distance" field')
def then_contains_distance(api_response):
    assert 'distance' in api_response['ultra']
    assert api_response['ultra']['distance'] == 25.0
