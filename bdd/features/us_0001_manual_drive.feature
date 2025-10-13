Feature: US_0001 Manual Drive Control
    As an End User,
    I want to control the robot’s movement (forward, reverse, left, right, stop) with adjustable speed,
    so that I can navigate the robot accurately and enjoy responsive handling.

    Scenario: Sending a forward command
        Given the robot is connected and ready
        When I send a "forward" command
        Then the robot should move forward
        And the command should be acknowledged

    Scenario: Adjusting the speed
        Given the robot is connected and ready
        When I set the speed to 50
        Then the speed should be updated
        And the command should be acknowledged

    Scenario: Sending a stop command
        Given the robot is moving
        When I send a "DS" command
        Then the robot should stop moving
        And the command should be acknowledged

    Scenario: Command with invalid speed
        Given the robot is connected and ready
        When I set the speed to 150
        Then the speed should be clamped to the maximum
        And the command should be acknowledged

