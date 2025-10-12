Feature: US-0001: Manual Robot Control
  As a user, I want to control the robot's movement manually through the web interface
  so that I can navigate it in real-time.

  Scenario: Command triggers movement within acceptable latency
    Given the web client is connected to the robot and clocks are synchronized
    When the user sends a drive command "forward" with speed 1.0
    And the controller receives the command
    Then the robot should start moving in the "forward" direction within 100 milliseconds of the command timestamp
    And telemetry contains a command-received timestamp and a motor-start timestamp

  Scenario: Speed scaling is applied proportionally
    Given the web client is connected to the robot and clocks are synchronized
    And the user sends a drive command "forward" with speed 0.5
    When the controller receives the command
    Then motor output shall be proportional to 0.5 within a tolerance of 5 percent

  Scenario: All directions are available via the web UI
    Given the main control UI is loaded
    When the user inspects movement controls
    Then controls for forward, reverse, left, right, and stop are present and operable

  Scenario: Out-of-range commands are clamped and logged
    Given the web client is connected to the robot and clocks are synchronized
    And the user sends a drive command "forward" with speed 1.5
    When the controller receives the command
    Then the controller clamps speed to the configured maximum and logs an event
