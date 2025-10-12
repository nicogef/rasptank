# User Stories

This document provides an overview of the user stories for the RaspTank project. Each user story is detailed in its own file for better organization and maintainability.

## List of User Stories

- **[US_0001: Manual Drive Control](user_stories/us_0001_manual_drive.md)**  
  As an End User, I want to control the robot’s movement (forward, reverse, left, right, stop) with adjustable speed, so that I can navigate the robot accurately and enjoy responsive handling.  
  *Related Requirements:* FR_001, NFR_003, NFR_005

- **[US_0002: Gimbal/Servo Control](user_stories/us_0002_gimbal_servo_control.md)**  
  As an End User, I want to control the camera gimbal (pan/tilt) with configurable limits and centering, so that I can aim the camera for better situational awareness during navigation.  
  *Related Requirements:* FR_002, NFR_003, NFR_005

- **[US_0003: LED/Lighting Control](user_stories/us_0003_led_lighting_control.md)**  
  As an End User, I want to control onboard LEDs for illumination and status indication, so that I can enhance visibility and monitor robot state.  
  *Related Requirements:* FR_003, NFR_005

- **[US_0004: FPV Video Stream](user_stories/us_0004_fpv_video_stream.md)**  
  As an End User, I want to view live camera video with adjustable quality, so that I can monitor the robot's environment in real-time.  
  *Related Requirements:* FR_004, NFR_003

- **[US_0005: Preset Motions](user_stories/us_0005_preset_motions.md)**  
  As an End User, I want preset movement patterns (e.g., square, figure-eight), so that I can demonstrate robot capabilities easily.  
  *Related Requirements:* FR_008

- **[US_0006: Sensor Integration](user_stories/us_0006_sensor_integration.md)**  
  As an End User, I want access to ultrasonic sensor readings, so that I can detect obstacles and enhance navigation.  
  *Related Requirements:* FR_005

- **[US_0007: Web Control UI](user_stories/us_0007_web_control_ui.md)**  
  As an End User, I want a web interface for full robot control, so that I can operate it from any supported browser.  
  *Related Requirements:* FR_007, NFR_005

## How to Use This Documentation

- Each user story file contains detailed information including feature items, acceptance criteria, traceability, testing strategy, code modules, design artifacts, and implementation tasks.
- For traceability to requirements, see `documentation/requirements.md`.
- For the overall process, see `documentation/project_structure.md`.

## Last Updated
October 12, 2025
