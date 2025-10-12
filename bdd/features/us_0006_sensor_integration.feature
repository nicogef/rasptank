Feature: US_0006 Sensor Integration
    As an End User,
    I want access to ultrasonic sensor readings,
    so that I can detect obstacles and enhance navigation.

    Scenario: Reading distance from an available sensor
        Given the robot has an ultrasonic sensor connected
        When I request the sensor distance
        Then I should receive a distance reading
        And the reading should be a positive number

    Scenario: Handling a missing sensor
        Given the robot does not have an ultrasonic sensor connected
        When I request the sensor distance
        Then the system should report the sensor as unavailable
        And the application should not crash

    Scenario: Sensor data is exposed via an API
        Given the robot system is running with a sensor
        When I query the "get_info" API endpoint
        Then the response should contain sensor data
        And the sensor data should include a "distance" field

