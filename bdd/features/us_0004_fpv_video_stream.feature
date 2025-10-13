Feature: US_0004 FPV Video Stream
    As an End User,
    I want to view live camera video with adjustable quality,
    so that I can monitor the robot's environment in real-time.

    Scenario: Starting the video stream
        Given the camera is available
        When I access the video feed
        Then I should receive a video stream
        And the stream should be in MJPEG format

    Scenario: Adjusting video quality
        Given the camera is streaming
        When I set the resolution to 640x480
        Then the video resolution should be updated
        And the stream should continue

    Scenario: Handling camera unavailability
        Given the camera is not available
        When I access the video feed
        Then the system should report camera unavailability
        And the application should not crash

