Feature: US_0007 Web Control UI
    As an End User,
    I want a web interface for full robot control,
    so that I can operate it from any supported browser.

    Scenario: Connecting to the robot via WebSocket
        Given the web UI is loaded
        When I enter connection details and click connect
        Then I should be connected to the robot
        And the status should show "Connected"

    Scenario: Sending a movement command
        Given I am connected to the robot
        When I click the forward button
        Then the forward command should be sent
        And the command should be logged

    Scenario: Adjusting speed
        Given I am connected to the robot
        When I set the speed slider to 75
        Then the speed should be updated
        And the command should be logged

    Scenario: Requesting system info
        Given I am connected to the robot
        When I click the "Get Info" button
        Then I should receive system information
        And the info should be displayed

