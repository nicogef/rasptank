# RaspTank – High‑Level Requirements

This document outlines high‑level, product‑oriented requirements for the Adeept RaspTank project. It is intended to guide design, implementation, testing, and operations. Items are intentionally technology‑agnostic unless a specific technology is core to the product.

## 1. Functional Requirements
- FR‑1: Manual Drive Control
  - The system shall provide forward, reverse, left, right, and stop commands with proportional speed control.
- FR‑2: Gimbal/Servo Control
  - The system shall provide pan/tilt control for the camera/servo assembly with configurable limits and centering.
- FR‑3: LED/Lighting Control
  - The system shall support turning LEDs on/off and, where supported, brightness control.
- FR‑4: FPV Video Stream
  - The system shall stream live camera video to a client over the network with adjustable resolution and frame rate.
- FR‑5: Sensor Integration (if equipped)
  - The system shall expose distance/ultrasonic readings and make them available to client applications.
- FR‑6: Programmatic API
  - The system shall provide a Python API to control motors, servos, LEDs, and read sensors, suitable for use in scripts and tests.
- FR‑7: Web Control UI
  - The system shall provide a web interface to control the robot and view telemetry/stream on supported platforms.
- FR‑8: Preset Motions
  - The system shall support basic movement macros (e.g., square/figure‑eight), and servo poses.

## 2. Non‑Functional Requirements
- NFR‑1: Compatibility
  - Support Raspberry Pi models 3B/3B+/4/5 and compatible HATs as listed by the project.
- NFR‑2: Operating System
  - Support Raspberry Pi OS (Bullseye/Bookworm) with current LTS kernel; document dependencies.
- NFR‑3: Performance
  - Control loop latency under 50 ms on a Pi 4 for basic drive/servo commands.
  - Video streaming at 640×480 20 FPS or higher on a Pi 4 under default settings.
- NFR‑4: Reliability
  - The robot shall recover gracefully from transient I2C/SPI errors without requiring a reboot.
- NFR‑5: Usability
  - The default UI shall be operable from a mobile browser; basic functions shall be reachable within two clicks/taps.
- NFR‑6: Observability
  - Provide structured logs for key events (startup, device init, command exec, faults) and an option for debug logs.
- NFR‑7: Security (Baseline)
  - Web interface shall support optional authentication; credentials must not be hard‑coded in source.
  - Network services shall bind to a configurable host/port; default to localhost or LAN‑safe settings.
- NFR‑8: Configurability
  - Expose configuration via a file and environment variables for pins, PWM frequencies, channel mappings, and limits.
- NFR‑9: Portability
  - The Python API shall not require root unless device access mandates it; document when sudo is necessary.

## 3. Hardware/Control Requirements
- HWR‑1: Motor Control
  - PWM frequency and duty cycle ranges shall be configurable per motor driver.
  - Support differential drive with independent left/right control.
- HWR‑2: Servo Control
  - Provide min/max pulse width calibration and safe ranges; clamp outputs to calibrated bounds.
- HWR‑3: I2C/SPI Abstraction
  - Abstract hardware access behind controller interfaces to enable mocking in unit tests.
- HWR‑4: Power‑On Safety
  - On startup, motors shall be stopped and servos centered within safe ranges.

## 4. Safety Requirements
- SFR‑1: Watchdog/Fail‑Safe
  - If no control command is received within a configurable timeout, the system shall stop motors.
- SFR‑2: Limit Enforcement
  - The system shall enforce configured servo travel limits and motor duty cycle caps.
- SFR‑3: Emergency Stop
  - Provide an immediate stop command/API that halts all motion, bypassing queued actions.

## 5. Software Quality Requirements
- SQR‑1: Code Quality
  - Maintain linting and formatting standards (e.g., Ruff/Flake8, Black) via CI checks.
- SQR‑2: Testing
  - Provide unit tests with hardware mocked; achieve and maintain an agreed minimum coverage (e.g., ≥80% of control logic).
- SQR‑3: CI/CD
  - Provide a GitHub Actions workflow to run tests and quality checks on pull requests and main.
- SQR‑4: Documentation
  - README shall include quick start, hardware setup, and troubleshooting; API docs or docstrings for public interfaces.

## 6. Deployment/Operations Requirements
- DOR‑1: Installation
  - Provide a pyproject/setup with dependencies; support pip install from source.
- DOR‑2: Configuration Management
  - Provide example configuration and clear instructions for overriding defaults.
- DOR‑3: Service Management
  - Provide an optional systemd service example for headless boot operation.

## 7. Extensibility Requirements
- EXT‑1: Modularity
  - Controllers (motors, servos, LEDs, sensors) shall be modular and replaceable with alternate implementations.
- EXT‑2: Plugin/Adapter Pattern
  - Hardware drivers shall implement a documented interface allowing drop‑in mocks for tests and alternates for real hardware.

## 8. Telemetry & Diagnostics Requirements
- TDR‑1: Health Checks
  - Provide a simple endpoint or CLI to report device initialization status and connectivity to hardware buses.
- TDR‑2: Debug Utilities
  - Provide scripts/commands for calibrating servos and testing motors without the full web stack.

## 9. Internationalization/Localization (Optional)
- I18N‑1: UI Text
  - Structure web UI strings to be replaceable for future localization.

## 10. Compliance & Licensing
- CPL‑1: Licensing
  - Include and honor appropriate open‑source licenses for project code and third‑party dependencies.

---

Change management: This document is expected to evolve. Proposals should be made via pull request, and requirements should be traceable to implementation (code, tests, or docs) whenever practical.