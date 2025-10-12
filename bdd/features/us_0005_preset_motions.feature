Feature: US_0005 Preset Motions
    As an End User,
    I want preset movement patterns (e.g., square, figure-eight),
    so that I can demonstrate robot capabilities easily.

    Scenario: Starting automatic obstacle avoidance
        Given the robot is ready for preset motions
        When I start the automatic mode
        Then the robot should begin obstacle avoidance
        And the command should be acknowledged

    Scenario: Stopping preset motion
        Given the robot is in preset motion
        When I stop the preset motion
        Then the robot should stop moving
        And the command should be acknowledged

    Scenario: Switching to track line mode
        Given the robot is ready for preset motions
        When I start the track line mode
        Then the robot should begin following a line
        And the command should be acknowledged

