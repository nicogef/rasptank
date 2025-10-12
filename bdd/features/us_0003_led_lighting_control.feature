Feature: US_0003 LED/Lighting Control
    As an End User,
    I want to control onboard LEDs for illumination and status indication,
    so that I can enhance visibility and monitor robot state.

    Scenario: Setting all LEDs to red
        Given the LED controller is initialized
        When I set all LEDs to red
        Then all LEDs should be red
        And the command should be acknowledged

    Scenario: Setting LED brightness
        Given the LED controller is initialized
        When I set the brightness to 50
        Then the brightness should be updated
        And the command should be acknowledged

    Scenario: Resetting LEDs to default
        Given the LED controller is initialized
        When I reset the LEDs
        Then the LEDs should return to default state
        And the command should be acknowledged

