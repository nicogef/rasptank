Feature: US_0002 Gimbal/Servo Control
    As an End User,
    I want to control the camera gimbal (pan/tilt) with configurable limits and centering,
    so that I can aim the camera for better situational awareness during navigation.

    Scenario: Moving the camera up
        Given the camera servo is initialized
        When I send an "up" command
        Then the camera should move up
        And the command should be acknowledged

    Scenario: Centering the camera
        Given the camera servo is initialized
        When I send a "home" command
        Then the camera should return to center position
        And the command should be acknowledged

    Scenario: Moving the camera to a specific angle
        Given the camera servo is initialized
        When I move the camera to angle 90
        Then the camera should be at angle 90
        And the command should be acknowledged

