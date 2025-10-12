# User Stories

## US_0001: Manual Drive Control

**ID:** US_0001

**Title:** Manual Drive Control

**What & Why:**
As an End User, I want to control the robot’s movement (forward, reverse, left, right, stop) with adjustable speed, so that I can navigate the robot accurately and enjoy responsive handling.

### Feature Items (How & Who)
- **US_0001_FI_0001:** Drive command processing
  - How: backend controller command parser → motor interface; validate commands, map to motor velocities, enforce safety limits, apply speed scaling
  - Who: Software Engineer / `src/rasptank_controls.py`
- **US_0001_FI_0002:** Web UI controls & client-side command publishing
  - How: button/joystick UI emits normalized drive commands over WebSocket/API
  - Who: Web Developer / `controller_web/main.js`
- **US_0001_FI_0003:** Real-time transport
  - How: WebSocket handler with lightweight acks and timestamps
  - Who: Software Engineer / `src/web_server.py`
- **US_0001_FI_0004:** Safety & limits enforcement
  - How: watchdog and clamp logic in controller and hardware interfaces
  - Who: Robotics Engineer + Software Engineer / `src/rasptank_controls.py`, `src/hardware/*`
- **US_0001_FI_0005:** Observability & telemetry for verification
  - How: timestamped command/ack events and telemetry endpoint
  - Who: Software Engineer / `src/web_server.py`, `src/rasptank_controls.py`

### Acceptance Criteria (BDD scenarios)
- **US_0001_AC_0001:** Drive command input results in robot movement within 50 ms (95th percentile)
- **US_0001_AC_0002:** Speed control reflects input (proportional scaling within ±5% tolerance)
- **US_0001_AC_0003:** Web UI exposes controls for forward, reverse, left, right, and stop and they are operable
- **US_0001_AC_0004:** Commands exceeding configured limits are clamped and logged

### Traceability
- Related requirements: `FR_001` (Manual Drive Control), `NFR_003` (Performance), `NFR_005` (Usability)
- Related user story items: US_0001_FI_0001..0005

### Testing Strategy
- **Test Types:** Unit, Integration, End-to-End, Performance, Manual
- **BDD Artifacts (stored under `bdd/`):**
  - Feature file: `bdd/features/us_0001_manual_drive.feature`
  - Step definitions: `bdd/steps/us_0001_steps.py`
- **Unit tests:**
  - `tests/test_rasptank_control.py` — add tests for speed scaling, clamping, and command mapping
- **Integration/E2E tests:**
  - `bdd/` E2E scenarios (run in CI or dedicated hardware environment) to validate latency and telemetry
  - `tests/test_webpage_clicks_e2e.py` — UI interactions validated against mock or real backend
- **Test Approach per AC:**
  - AC_0001 (latency ≤ 50 ms): measure command-received → motor-start timestamps; verify 95th percentile ≤ 50 ms. Use integration tests with mock server in CI and hardware tests in dedicated environment.
  - AC_0002 (speed scaling): unit tests for mapping function + hardware-in-loop verification.
  - AC_0003 (UI coverage): browser automation (Playwright/Selenium) or mock server + manual acceptance tests.
  - AC_0004 (clamping): unit tests for clamping logic + integration test for log emission when out-of-range commands received.

### Code modules
- Implementation: `src/rasptank_controls.py`, `src/web_server.py`, `controller_web/main.js`, `src/hardware/*`
- Tests: `tests/*` (unit) and `bdd/*` (BDD scenarios)

### Design artifacts to produce
- WebSocket message schema: `documentation/design/us_0001_ws_api.md`
- Sequence diagram: `documentation/design/us_0001_sequence.svg`
- Drive command lifecycle diagram and safety checklist: `documentation/design/us_0001_flow.md`

### Implementation tasks (backlog suggestions)
- T1: Implement/verify `process_drive_command()` with speed scaling and limits (US_0001_FI_0001)
- T2: Implement client-side `sendDriveCommand()` and telemetry hooks (US_0001_FI_0002)
- T3: Add timestamps/acks on transport and telemetry (US_0001_FI_0003 and FI_0005)
- T4: Add unit tests and BDD feature + step defs (US_0001_FI_0001..0003)
- T5: Schedule performance test on hardware and collect baseline latency metrics (US_0001_FI_0005)

---

// End of US_0001

