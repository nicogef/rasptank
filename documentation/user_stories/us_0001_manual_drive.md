# US_0001: Manual Drive Control

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
- **US_0001_AC_0001:** Drive command input results in robot movement within 50 ms (95th percentile latency from command receipt to motor start).
- **US_0001_AC_0002:** Speed control reflects input with proportional scaling within ±5% tolerance (e.g., speed 0.5 results in 50% motor output ±2.5%).
- **US_0001_AC_0003:** Web UI exposes operable controls for forward, reverse, left, right, and stop, with each button triggering the corresponding command within 1 second of click.
- **US_0001_AC_0004:** Commands exceeding configured limits (e.g., speed >1.0) are clamped to maximum values and logged as WARN events.

### Traceability
- Related requirements: `FR_001` (Manual Drive Control), `NFR_003` (Performance), `NFR_005` (Usability)
- Related user story items: US_0001_FI_0001..0005
- Links back: See `documentation/requirements.md` for FR_001 details.

### Testing Strategy
- **Test Types:** Unit, Integration, End-to-End, Performance, Manual
- **BDD Artifacts (stored under `bdd/`):**
  - Feature file: `bdd/features/us_0001_manual_drive.feature`
  - Step definitions: `bdd/steps/test_us_0001_manual_drive.py`
- **Unit tests:**
  - `tests/test_rasptank_control.py` — add tests for speed scaling, clamping, and command mapping
- **Integration/E2E tests:**
  - `bdd/` E2E scenarios (run in CI or dedicated hardware environment) to validate latency and telemetry
  - `tests/test_webpage_clicks_e2e.py` — UI interactions validated against mock or real backend
- **Coverage Goals:** Achieve ≥80% code coverage for `src/rasptank_controls.py` and related modules.
- **Test Approach per AC:**
  - AC_0001 (latency ≤ 50 ms): measure command-received → motor-start timestamps; verify 95th percentile ≤ 50 ms. Use integration tests with mock server in CI and hardware tests in dedicated environment.
  - AC_0002 (speed scaling): unit tests for mapping function + hardware-in-loop verification on Pi 3B, 4, and 5.
  - AC_0003 (UI coverage): browser automation (Playwright/Selenium) or mock server + manual acceptance tests; test on mobile viewport (360–414 px).
  - AC_0004 (clamping): unit tests for clamping logic + integration test for log emission when out-of-range commands received; verify no hardware damage.

### Code modules
- Implementation: `src/rasptank_controls.py`, `src/web_server.py`, `controller_web/main.js`, `src/hardware/*`
- Tests: `tests/*` (unit) and `bdd/*` (BDD scenarios)

### Design Artifacts

#### WebSocket Message Schema
This describes the WebSocket message schema for drive commands in US_0001.

**Message Format**
- **Type:** JSON
- **Direction:** Client → Server
- **Fields:**
  - `command`: String (e.g., "forward", "stop")
  - `speed`: Float (0.0 to 1.0)
  - `timestamp`: Integer (Unix timestamp in milliseconds)

**Example**
```json
{
  "command": "forward",
  "speed": 0.8,
  "timestamp": 1699999999999
}
```

**Response**
Server acknowledges with:
```json
{
  "status": "ok",
  "timestamp": 1699999999999
}
```

#### Sequence Diagram
This should contain a sequence diagram showing the flow of drive commands from UI to hardware.

**Placeholder Description**
- User clicks button in web UI
- Web UI sends WebSocket message to server
- Server processes command via rasptank_controls.py
- Command sent to motor controller
- Hardware responds

*Note: Replace with actual SVG diagram.*

#### Drive Command Lifecycle and Safety Checklist

**Lifecycle Diagram**
1. User input (UI button/joystick)
2. Client-side validation and normalization
3. WebSocket transmission
4. Server receipt and parsing
5. Controller processing (speed scaling, clamping)
6. Hardware command execution
7. Telemetry logging

**Safety Checklist**
- [ ] Speed clamped to max 1.0
- [ ] Commands validated before hardware access
- [ ] Watchdog timer active
- [ ] Emergency stop available
- [ ] Logging enabled for diagnostics

*Note: This is a placeholder. Replace with actual diagram and checklist.*

### Implementation tasks (backlog suggestions)
- **T1:** Implement/verify `process_drive_command()` with speed scaling and limits (US_0001_FI_0001) — Priority: High, Effort: 2-3 days, Status: In Progress
- **T2:** Implement client-side `sendDriveCommand()` and telemetry hooks (US_0001_FI_0002) — Priority: High, Effort: 1-2 days, Status: Pending
- **T3:** Add timestamps/acks on transport and telemetry (US_0001_FI_0003 and FI_0005) — Priority: Medium, Effort: 1 day, Status: Pending
- **T4:** Add unit tests and BDD feature + step defs (US_0001_FI_0001..0003) — Priority: High, Effort: 2 days, Status: Completed
- **T5:** Schedule performance test on hardware and collect baseline latency metrics (US_0001_FI_0005) — Priority: Medium, Effort: 1 day, Status: Pending

### Last Updated
October 12, 2025

### Change Log
- October 12, 2025: Enhanced acceptance criteria with measurable details; added priority, effort, and status to tasks; expanded testing strategy with coverage goals and hardware testing; added cross-references and last updated field.
