# RaspTank — Requirements

This document defines the authoritative, high-level requirements for the RaspTank project, following the template in project_structure.md. Each requirement is atomic, testable, and traceable.

## Glossary
- **FR**: Functional Requirement - Describes what the system must do.
- **NFR**: Non-Functional Requirement - Describes how the system performs (e.g., performance, usability).
- **SFR**: Safety Requirement - Describes safety-related constraints.
- **HWR**: Hardware/Control Requirement - Describes hardware-specific needs.
- **SQR**: Software Quality Requirement - Describes code quality and testing standards.
- **DOR**: Deployment/Operations Requirement - Describes installation and operational needs.
- **EXT**: Extensibility Requirement - Describes modularity and future-proofing.
- **TDR**: Telemetry & Diagnostics Requirement - Describes monitoring and debugging needs.
- **I18N**: Internationalization/Localization Requirement - Describes localization readiness.
- **CPL**: Compliance & Licensing Requirement - Describes legal and licensing needs.

---

## 1. Functional Requirements (FR)

- FR_001 (Verified) - Manual Drive Control
  - The system shall provide forward, reverse, left, right, and stop commands with proportional speed control.
  - Rationale: Enables users to navigate the robot precisely and safely.
  - Verification: Test (Unit tests verify command mapping and scaling); Demonstration (Manual inspection of UI controls).
  - Acceptance criteria:
    - FR_001_AC_001: Drive commands are callable via Python API and web UI.
    - FR_001_AC_002: Speed scaling is observable in tests or mocks.
  - Traceability:
    - User Stories: US_0001
    - Tests: tests/test_rasptank_control.py, tests/controllers/
    - Code: src/rasptank_controls.py, src/controllers/motors.py, src/system.py, controller_web/
  - Status: Verified (2025-10-12)
  - Owner: Product Owner

- FR_002 (Verified) - Gimbal/Servo Control
  - The system shall provide pan/tilt control for the camera/servo assembly with configurable limits and centering.
  - Rationale: Enables aiming the camera for situational awareness.
  - Verification: Test (Unit tests for servo limits); Demonstration (Manual servo movement).
  - Acceptance criteria:
    - FR_002_AC_001: Pan/tilt angles are clamped to configured min/max with no overshoot beyond 2%.
    - FR_002_AC_002: Center command positions both axes within ±2° of midpoint.
    - FR_002_AC_003: Response latency ≤ 50 ms from UI action on Pi 4.
  - Traceability:
    - User Stories: US_0002
    - Tests: tests/controllers/test_servo.py
    - Code: src/controllers/servo.py, src/rasptank_controls.py
  - Status: Verified (2025-10-12)
  - Owner: Robotics Engineer

- FR_003 (Verified) - LED/Lighting Control
  - The system shall support turning LEDs on/off and, where supported, brightness control.
  - Rationale: Illumination and status indication.
  - Verification: Test (Unit tests for LED state); Demonstration (Manual LED toggle).
  - Acceptance criteria:
    - FR_003_AC_001: LED on/off reflected at hardware within 2 s.
    - FR_003_AC_002: Brightness adjustments map linearly (±10% tolerance) across at least 5 levels.
    - FR_003_AC_003: Controls available in main UI.
  - Traceability:
    - User Stories: US_0003
    - Tests: tests/controllers/test_leds.py
    - Code: src/controllers/leds.py
  - Status: Verified (2025-10-12)
  - Owner: Software Engineer

- FR_004 (Verified) - FPV Video Stream
  - The system shall stream live camera video to a client over the network with adjustable resolution and frame rate.
  - Rationale: Real‑time visual feedback for teleoperation.
  - Verification: Demonstration (Video stream test); Analysis (Frame rate measurement).
  - Acceptance criteria:
    - FR_004_AC_001: Stream starts within 3 s of accessing the video view.
    - FR_004_AC_002: Default quality ≥ 640×480 at 20 FPS on Pi 4.
    - FR_004_AC_003: Resolution and/or FPS can be set via configuration or UI.
  - Traceability:
    - User Stories: US_0004
    - Tests: tests/test_webpage_with_mock.py, tests/test_webpage_clicks_e2e.py
    - Code: src/web_server.py, web/*
  - Status: Verified (2025-10-12)
  - Owner: Web Developer

- FR_005 (Verified) - Sensor Integration
  - The system shall expose distance/ultrasonic readings and make them available to client applications.
  - Rationale: Obstacle awareness and telemetry.
  - Verification: Test (Unit tests for sensor data); Demonstration (Sensor reading display).
  - Acceptance criteria:
    - FR_005_AC_001: Distance values update at least every 100 ms when sensor present.
    - FR_005_AC_002: When data are unavailable, API/UI marks readings as unavailable without crash.
    - FR_005_AC_003: API endpoint or method documented and stable.
  - Traceability:
    - User Stories: US_0007
    - Tests: tests/test_system.py, tests/test_webpage_with_mock.py
    - Code: src/rasptank_controls.py, src/system.py, web/ultra.py
  - Status: Verified (2025-10-12)
  - Owner: Robotics Engineer

- FR_006 (Verified) - Programmatic API
  - The system shall provide a Python API to control motors, servos, LEDs, and read sensors, suitable for use in scripts and tests.
  - Rationale: Automation, testing, and extensibility.
  - Verification: Test (Unit tests for API calls); Inspection (API documentation).
  - Acceptance criteria:
    - FR_006_AC_001: Public methods exist for drive, servo, LED, and sensor access with docstrings.
    - FR_006_AC_002: API usable without root except where hardware mandates it.
    - FR_006_AC_003: Examples or tests demonstrate usage without the web UI.
  - Traceability:
    - User Stories: US_0001, US_0002, US_0003, US_0007
    - Tests: tests/test_rasptank_control.py, tests/controllers/*
    - Code: src/rasptank_controls.py, src/controllers/*
  - Status: Verified (2025-10-12)
  - Owner: Software Engineer

- FR_007 (Verified) - Web Control UI
  - The system shall provide a web interface to control the robot and view telemetry/stream on supported platforms.
  - Rationale: Primary user interface for most users.
  - Verification: Demonstration (UI interaction test); Test (E2E tests for controls).
  - Acceptance criteria:
    - FR_007_AC_001: UI exposes drive, servo, LED, and stream controls from a mobile browser.
    - FR_007_AC_002: Basic actions reachable within ≤ 2 clicks/taps.
    - FR_007_AC_003: Connection settings allow host/port configuration.
  - Traceability:
    - User Stories: US_0001, US_0002, US_0004, US_0005, US_0007
    - Tests: tests/test_webpage_clicks_e2e.py, tests/test_webpage_with_mock.py
    - Code: controller_web/*, src/web_server.py
  - Status: Verified (2025-10-12)
  - Owner: Web Developer

- FR_008 (Verified) - Preset Motions
  - The system shall support basic movement macros (e.g., square/figure‑eight) and servo poses.
  - Rationale: Demonstrations and convenience.
  - Verification: Test (Unit tests for motion sequences); Demonstration (Motion execution).
  - Acceptance criteria:
    - FR_008_AC_001: At least two preset drive patterns execute to completion within documented durations.
    - FR_008_AC_002: Completion feedback provided via API/UI log.
  - Traceability:
    - User Stories: US_0005
    - Tests: tests/test_rasptank_control.py::test_preset_motions (if present) or add tests
    - Code: src/rasptank_controls.py
  - Status: Verified (2025-10-12)
  - Owner: Software Engineer

## 2. Non-Functional Requirements (NFR)

- NFR_001 (Verified) - Compatibility
  - The system shall support Raspberry Pi models 3B/3B+/4/5 and compatible HATs as listed by the project.
  - Rationale: Ensure broad hardware support for users.
  - Verification: Inspection (Documentation check); Demonstration (Smoke test on one device per generation).
  - Acceptance criteria:
    - NFR_001_AC_001: Documentation lists supported models and any caveats.
    - NFR_001_AC_002: Smoke test completes on one device per supported generation.
  - Traceability:
    - Code: src/hardware/*, setup_HAT_V3.1.py
    - Tests: tests/test_system.py (env checks)
  - Status: Verified (2025-10-12)
  - Owner: Product Owner

- NFR_002 (Verified) - Operating System
  - The system shall support Raspberry Pi OS (Bullseye/Bookworm) with current LTS kernel and document dependencies.
  - Rationale: Align with maintained OS versions.
  - Verification: Inspection (Dependency documentation).
  - Acceptance criteria:
    - NFR_002_AC_001: README or docs list required packages and versions.
    - NFR_002_AC_002: Setup scripts complete without errors on supported OS versions.
  - Traceability:
    - Code: requirements.txt, setup.py, pyproject.toml
    - Tests: CI install step logs
  - Status: Verified (2025-10-12)
  - Owner: DevOps

- NFR_003 (Verified) - Performance
  - Control loop latency shall be under 50 ms on a Pi 4 for basic drive/servo commands, and video streaming shall achieve ≥ 640×480 at 20 FPS by default on Pi 4.
  - Rationale: Usability and responsiveness.
  - Verification: Test (Latency measurement); Analysis (Frame rate analysis); Demonstration (Performance test).
  - Acceptance criteria:
    - NFR_003_AC_001: Measured command‑to‑actuation latency ≤ 50 ms (median) with ≤ 5% > 75 ms outliers.
    - NFR_003_AC_002: Video default profile sustains ≥ 20 FPS for 60 s.
  - Traceability:
    - Code: src/rasptank_controls.py, src/web_server.py
    - Tests: tests/async_helper.py, tests/test_webpage_with_mock.py
  - Status: Verified (2025-10-12)
  - Owner: Architect

- NFR_004 (Verified) - Reliability
  - The robot shall recover gracefully from transient I2C/SPI errors without requiring a reboot.
  - Rationale: Robust operation on real hardware.
  - Verification: Test (Fault injection); Inspection (Error handling code).
  - Acceptance criteria:
    - NFR_004_AC_001: Hardware abstraction retries transient bus errors up to a configured limit.
    - NFR_004_AC_002: System logs error and resumes normal operation without crash.
  - Traceability:
    - Code: src/hardware/pca9685_controller.py, src/hardware/spi_controller.py
    - Tests: tests/test_system.py (fault injection if available)
  - Status: Verified (2025-10-12)
  - Owner: Robotics Engineer

- NFR_005 (Verified) - Usability
  - The default UI shall be operable from a mobile browser; basic functions shall be reachable within two clicks/taps.
  - Rationale: Ease of use for typical users.
  - Verification: Inspection (UI layout check); Demonstration (Mobile browser test).
  - Acceptance criteria:
    - NFR_005_AC_001: Drive/servo/LED controls accessible within ≤ 2 taps from landing page.
    - NFR_005_AC_002: UI layouts function on viewport width 360–414 px without horizontal scroll.
  - Traceability:
    - Code: controller_web/*
    - Tests: tests/test_webpage_clicks_e2e.py
  - Status: Verified (2025-10-12)
  - Owner: Web Developer

- NFR_006 (Approved) - Observability
  - The system shall provide structured logs for key events (startup, device init, command execution, faults) and an option for debug logs.
  - Rationale: Troubleshooting and operations.
  - Verification: Inspection (Logging code); Demonstration (Log output test).
  - Acceptance criteria:
    - NFR_006_AC_001: Logs include timestamp, level, and subsystem for listed events.
    - NFR_006_AC_002: Debug logging can be enabled via config or env var.
  - Traceability:
    - Code: src/system.py, src/web_server.py
    - Tests: tests/test_system.py (logging assertions)
  - Status: Approved
  - Owner: DevOps

- NFR_007 (Approved) - Security (Baseline)
  - The web interface shall support optional authentication; credentials shall not be hard‑coded; services shall bind to configurable host/port with safe defaults.
  - Rationale: Reduce exposure on networks and avoid secret leakage.
  - Verification: Inspection (Code review for hard-coded secrets); Test (Connection tests).
  - Acceptance criteria:
    - NFR_007_AC_001: No plaintext credentials in source; authentication (if enabled) uses configurable secrets.
    - NFR_007_AC_002: Default bind host is localhost or LAN‑safe; port configurable via env/config.
  - Traceability:
    - Code: src/web_server.py, controller_web/*
    - Tests: tests/test_webpage_with_mock.py (connection/handshake), scripts/mock_server.py
  - Status: Approved
  - Owner: Architect

- NFR_008 (Approved) - Configurability
  - The system shall expose configuration via a file and environment variables for pins, PWM frequencies, channel mappings, and limits.
  - Rationale: Adaptability to different HATs and setups.
  - Verification: Inspection (Config code); Test (Override tests).
  - Acceptance criteria:
    - NFR_008_AC_001: Configuration keys documented and read at startup.
    - NFR_008_AC_002: Environment variables can override file defaults.
  - Traceability:
    - Code: src/system.py, src/controllers/*
    - Tests: tests/test_system.py
  - Status: Approved
  - Owner: Architect

- NFR_009 (Approved) - Portability
  - The Python API shall not require root unless device access mandates it; documentation shall state when sudo is necessary.
  - Rationale: Developer experience and security principle of least privilege.
  - Verification: Inspection (API code); Demonstration (Non-root usage test).
  - Acceptance criteria:
    - NFR_009_AC_001: Non‑privileged operations (mock mode) run without sudo.
    - NFR_009_AC_002: Documentation clearly flags privileged operations.
  - Traceability:
    - Code: src/hardware/*, src/controllers/*
    - Tests: tests/controllers/* (mocked)
  - Status: Approved
  - Owner: DevOps

## 3. Hardware/Control Requirements

- HWR_001 (Approved) - Motor Control
  - PWM frequency and duty cycle ranges shall be configurable per motor driver and support differential drive with independent left/right control.
  - Rationale: Support diverse drivers and tunable behavior.
  - Verification: Test (PWM configuration tests); Inspection (Driver code).
  - Acceptance criteria:
    - HWR_001_AC_001: Frequency and duty limits are settable and enforced.
    - HWR_001_AC_002: Left/right channels operate independently with common drive API.
  - Traceability:
    - Code: src/controllers/motors.py, src/hardware/pca9685_controller.py
    - Tests: tests/controllers/test_motors.py
  - Status: Approved
  - Owner: Robotics Engineer

- HWR_002 (Approved) - Servo Control
  - The system shall provide min/max pulse width calibration and safe ranges; outputs are clamped to calibrated bounds.
  - Rationale: Prevent mechanical damage and ensure repeatability.
  - Verification: Test (Calibration tests); Inspection (Servo code).
  - Acceptance criteria:
    - HWR_002_AC_001: Calibration values persisted or configurable.
    - HWR_002_AC_002: Commands beyond range are clamped; no hardware jitter beyond ±2%.
  - Traceability:
    - Code: src/controllers/servo.py
    - Tests: tests/controllers/test_servo.py
  - Status: Approved
  - Owner: Robotics Engineer

- HWR_003 (Approved) - I2C/SPI Abstraction
  - Hardware access shall be abstracted behind controller interfaces to enable mocking in unit tests.
  - Rationale: Testability and portability.
  - Verification: Inspection (Interface code); Test (Mocked tests).
  - Acceptance criteria:
    - HWR_003_AC_001: Controllers expose interfaces that can be replaced with mocks.
    - HWR_003_AC_002: Unit tests run without physical hardware attached.
  - Traceability:
    - Code: src/hardware/*, src/controllers/*
    - Tests: tests/controllers/mock_controller.py; tests/controllers/*
  - Status: Approved
  - Owner: Architect

- HWR_004 (Approved) - Power‑On Safety
  - On startup, motors shall be stopped and servos centered within safe ranges.
  - Rationale: Prevent unintended motion.
  - Verification: Test (Startup tests); Inspection (Init code); Demonstration (Boot sequence).
  - Acceptance criteria:
    - HWR_004_AC_001: Boot sequence sets motor outputs to neutral/off.
    - HWR_004_AC_002: Servos center within ±2° of configured midpoint.
  - Traceability:
    - Code: src/system.py, src/rasptank_controls.py
    - Tests: tests/test_system.py
  - Status: Approved
  - Owner: Robotics Engineer

## 4. Safety Requirements

- SFR_001 (Approved) - Watchdog/Fail‑Safe
  - If no control command is received within a configurable timeout, the system shall stop motors.
  - Rationale: Reduce risk of runaway behavior.
  - Verification: Test (Timeout tests); Demonstration (Fail-safe activation).
  - Acceptance criteria:
    - SFR_001_AC_001: With timeout set to T, motors stop within T + 100 ms without new commands.
    - SFR_001_AC_002: Event is logged with severity warning or higher.
  - Traceability:
    - Code: src/system.py, src/rasptank_controls.py
    - Tests: tests/test_system.py
  - Status: Approved
  - Owner: Architect

- SFR_002 (Approved) - Limit Enforcement
  - The system shall enforce configured servo travel limits and motor duty cycle caps.
  - Rationale: Safety and hardware protection.
  - Verification: Test (Limit tests); Inspection (Enforcement code).
  - Acceptance criteria:
    - SFR_002_AC_001: Attempts to exceed limits are clamped; no commands exceed configured caps.
    - SFR_002_AC_002: Violations are optionally logged at debug level for diagnostics.
  - Traceability:
    - Code: src/controllers/servo.py, src/controllers/motors.py
    - Tests: tests/controllers/test_servo.py, tests/controllers/test_motors.py
  - Status: Approved
  - Owner: Robotics Engineer

- SFR_003 (Approved) - Emergency Stop
  - The system shall provide an immediate stop command/API that halts all motion, bypassing queued actions.
  - Rationale: Rapid response to hazards.
  - Verification: Test (E-stop tests); Demonstration (Emergency stop activation).
  - Acceptance criteria:
    - SFR_003_AC_001: E‑stop API halts motors within 100 ms from invocation.
    - SFR_003_AC_002: E‑stop is reachable from UI in ≤ 1 tap from the main control view.
  - Traceability:
    - Code: src/rasptank_controls.py, controller_web/*
    - Tests: tests/test_webpage_clicks_e2e.py, tests/test_rasptank_control.py
  - Status: Approved
  - Owner: Architect

## 5. Software Quality Requirements

- SQR_001 (Approved) - Code Quality
  - The project shall maintain linting and formatting standards via CI checks.
  - Rationale: Maintainability and consistency.
  - Verification: Test (CI lint/format checks); Inspection (Code review).
  - Acceptance criteria:
    - SQR_001_AC_001: CI fails on lint errors; formatting enforced by Black.
    - SQR_001_AC_002: Lint configuration is documented in pyproject.toml or equivalent.
  - Traceability:
    - Code: pyproject.toml, scripts/ci.py
    - Tests: CI logs
  - Status: Approved
  - Owner: DevOps

- SQR_002 (Approved) - Testing
  - The project shall provide unit tests with hardware mocked and achieve a minimum of 80% coverage of control logic.
  - Rationale: Confidence in changes without hardware.
  - Verification: Test (Coverage report).
  - Acceptance criteria:
    - SQR_002_AC_001: pytest‑cov reports ≥ 80% coverage on src/ controllers and system logic.
    - SQR_002_AC_002: Tests run headless in CI.
  - Traceability:
    - Code: tests/**, scripts/ci.py
    - Tests: pytest coverage report, coverage.xml
  - Status: Approved
  - Owner: QA/Tester

- SQR_003 (Approved) - CI/CD
  - The project shall run tests and quality checks on pull requests and main.
  - Rationale: Prevent regressions.
  - Verification: Inspection (CI workflow).
  - Acceptance criteria:
    - SQR_003_AC_001: GitHub Actions workflow triggers on PR and push to main.
    - SQR_003_AC_002: Artifacts (coverage, junit) published in CI.
  - Traceability:
    - Code: .github/workflows/*, scripts/ci.py
  - Status: Approved
  - Owner: DevOps

- SQR_004 (Approved) - Documentation
  - The README shall include quick start, hardware setup, and troubleshooting; public APIs have docstrings.
  - Rationale: Onboarding and support.
  - Verification: Inspection (README and code).
  - Acceptance criteria:
    - SQR_004_AC_001: README contains sections: Quick Start, Hardware Setup, Troubleshooting.
    - SQR_004_AC_002: Public classes/functions in src/ have docstrings.
  - Traceability:
    - Code: README.md, src/**
    - Tests: docs lint (manual inspection)
  - Status: Approved
  - Owner: Product Owner

## 6. Deployment/Operations Requirements

- DOR_001 (Approved) - Installation
  - The project shall provide a pyproject/setup with dependencies and support pip install from source.
  - Rationale: Ease of installation.
  - Verification: Demonstration (Pip install test); Inspection (Setup files).
  - Acceptance criteria:
    - DOR_001_AC_001: `pip install .` succeeds in a clean venv on supported Python.
    - DOR_001_AC_002: Runtime dependencies installed automatically.
  - Traceability:
    - Code: pyproject.toml, setup.py, requirements.txt
    - Tests: CI install logs
  - Status: Approved
  - Owner: DevOps

- DOR_002 (Approved) - Configuration Management
  - The project shall provide example configuration and clear instructions for overriding defaults.
  - Rationale: Operator efficiency and reproducibility.
  - Verification: Inspection (Config docs); Demonstration (Override test).
  - Acceptance criteria:
    - DOR_002_AC_001: Example config file exists and is referenced in README.
    - DOR_002_AC_002: Overrides via environment variables documented and take effect at runtime.
  - Traceability:
    - Code: README.md, src/system.py
    - Tests: tests/test_system.py
  - Status: Approved
  - Owner: DevOps

- DOR_003 (Approved) - Service Management
  - The project shall provide an optional systemd service example for headless boot operation.
  - Rationale: Hands‑off startup for field use.
  - Verification: Inspection (Service file); Demonstration (Service start).
  - Acceptance criteria:
    - DOR_003_AC_001: A sample .service file exists with instructions.
    - DOR_003_AC_002: Service starts web/control stack at boot on Raspberry Pi OS when enabled.
  - Traceability:
    - Code: documentation (service example), src/web_server.py
  - Status: Approved
  - Owner: DevOps

## 7. Extensibility Requirements

- EXT_001 (Approved) - Modularity
  - Controllers (motors, servos, LEDs, sensors) shall be modular and replaceable with alternate implementations.
  - Rationale: Hardware variability and future upgrades.
  - Verification: Inspection (Interface code); Test (Replacement tests).
  - Acceptance criteria:
    - EXT_001_AC_001: Interfaces documented to allow drop‑in replacements.
    - EXT_001_AC_002: Mock implementations used in tests without code changes.
  - Traceability:
    - Code: src/controllers/*
    - Tests: tests/controllers/mock_controller.py
  - Status: Approved
  - Owner: Architect

- EXT_002 (Approved) - Plugin/Adapter Pattern
  - Hardware drivers shall implement a documented interface allowing drop‑in mocks for tests and alternates for real hardware.
  - Rationale: Maintainable hardware abstraction.
  - Verification: Inspection (Adapter code); Test (Mock swap tests).
  - Acceptance criteria:
    - EXT_002_AC_001: Adapter interface documented with example implementations.
    - EXT_002_AC_002: Tests swap real vs. mock via configuration.
  - Traceability:
    - Code: src/hardware/*, src/controllers/*
    - Tests: tests/controllers/*, tests/test_system.py
  - Status: Approved
  - Owner: Architect

## 8. Telemetry & Diagnostics Requirements

- TDR_001 (Approved) - Health Checks
  - The system shall provide a simple endpoint or CLI to report device initialization status and connectivity to hardware buses.
  - Rationale: Operational visibility.
  - Verification: Demonstration (Health check test); Test (Endpoint tests).
  - Acceptance criteria:
    - TDR_001_AC_001: Health endpoint/command returns OK/Degraded/Error with details.
    - TDR_001_AC_002: Includes at least I2C/SPI connectivity and controller init status.
  - Traceability:
    - Code: src/system.py, src/web_server.py, scripts/debug_open.py
    - Tests: tests/test_system.py
  - Status: Approved
  - Owner: DevOps

- TDR_002 (Approved) - Debug Utilities
  - The system shall provide scripts/commands for calibrating servos and testing motors without the full web stack.
  - Rationale: Hardware bring‑up and troubleshooting.
  - Verification: Demonstration (Calibration/test run); Inspection (Script code).
  - Acceptance criteria:
    - TDR_002_AC_001: Script exists to sweep servos with configurable bounds.
    - TDR_002_AC_002: Script exists to run motors forward/reverse at specified duty cycles.
  - Traceability:
    - Code: scripts/**
    - Tests: manual demonstration steps documented
  - Status: Approved
  - Owner: Robotics Engineer

## 9. Internationalization/Localization (Optional)

- I18N_001 (Approved) - UI Text Localization Readiness
  - UI strings shall be structured to be replaceable for future localization.
  - Rationale: Potential international users.
  - Verification: Inspection (UI code).
  - Acceptance criteria:
    - I18N_001_AC_001: UI text is centralized or wrapped for substitution.
    - I18N_001_AC_002: No hardcoded concatenations that impede translation for primary labels.
  - Traceability:
    - Code: controller_web/*
  - Status: Approved
  - Owner: Web Developer

## 10. Compliance & Licensing

- CPL_001 (Approved) - Licensing
  - The project shall include and honor appropriate open‑source licenses for project code and third‑party dependencies.
  - Rationale: Legal compliance and community norms.
  - Verification: Inspection (LICENSE file and dependencies).
  - Acceptance criteria:
    - CPL_001_AC_001: LICENSE file exists at repository root; third‑party licenses are documented if required.
    - CPL_001_AC_002: Dependencies are compatible with project license.
  - Traceability:
    - Code: LICENSE, requirements.txt, pyproject.toml
  - Status: Approved
  - Owner: Product Owner

---

Change management:
- Propose edits via pull request with status updates (Proposed → Approved → Implemented → Verified) and update traceability links to code and tests.
- Maintain numbering stability by appending new items at the end of each section.
