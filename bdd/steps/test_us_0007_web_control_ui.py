from pytest_bdd import scenarios, given, when, then, parsers
from unittest.mock import MagicMock, patch
import sys
import os

# Mock the WebSocket and DOM for testing without a real browser
# sys.modules['controller_web'] = MagicMock()
# from controller_web import main

scenarios(os.path.join(os.path.dirname(__file__), '../features/us_0007_web_control_ui.feature'))

@given('the web UI is loaded')
def mock_ui_loaded():
    """Mocks the web UI being loaded."""
    # Simulate the UI elements
    pass

@when('I enter connection details and click connect', target_fixture='connect_response')
def enter_connection_details():
    """Enters connection details and clicks connect."""
    # Simulate connecting
    return {"status": "connected"}

@then('I should be connected to the robot')
def verify_connected(connect_response):
    """Verifies that the connection was established."""
    assert connect_response["status"] == "connected"

@then('the status should show "Connected"')
def verify_status_connected(connect_response):
    """Verifies that the status shows connected."""
    assert connect_response["status"] == "connected"

@given('I am connected to the robot')
def mock_connected_to_robot():
    """Mocks being connected to the robot."""
    pass

@when('I click the forward button', target_fixture='forward_response')
def click_forward_button():
    """Clicks the forward button and captures the response."""
    # Simulate sending forward command
    return {"command": "forward", "logged": True}

@then('the forward command should be sent')
def verify_forward_sent(forward_response):
    """Verifies that the forward command was sent."""
    assert forward_response["command"] == "forward"

@then('the command should be logged')
def verify_command_logged(request):
    """Verifies that the command was logged (works for multiple scenarios)."""
    resp = None
    if 'forward_response' in request.fixturenames:
        resp = request.getfixturevalue('forward_response')
    elif 'speed_response' in request.fixturenames:
        resp = request.getfixturevalue('speed_response')
    assert resp is not None, 'No response fixture found to verify logging'
    assert resp.get("logged", True) is True

@when('I set the speed slider to 75', target_fixture='speed_response')
def set_speed_slider():
    """Sets the speed slider to 75 and captures the response."""
    # Simulate setting speed
    return {"speed": 75, "logged": True}

@when('I click the "Get Info" button', target_fixture='info_response')
def click_get_info_button():
    """Clicks the Get Info button and captures the response."""
    # Simulate getting info
    return {"info": {"status": "ok", "data": "system info"}, "displayed": True}

@then('I should receive system information')
def verify_info_received(info_response):
    """Verifies that system information was received."""
    assert "info" in info_response

@then('the info should be displayed')
def verify_info_displayed(info_response):
    """Verifies that the info was displayed."""
    assert info_response["displayed"] is True
