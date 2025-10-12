# US_0005: Preset Motions

**ID:** US_0005

**Title:** Preset Motions

**What & Why:**
As an End User, I want preset movement patterns (e.g., square, figure-eight), so that I can demonstrate robot capabilities easily.

### Feature Items (How & Who)
- **US_0005_FI_0001:** Motion pattern implementation
  - How: Sequence of drive commands with timing
  - Who: Software Engineer / `src/rasptank_controls.py`
- **US_0005_FI_0002:** Web UI preset controls
  - How: Buttons for starting presets
  - Who: Web Developer / `controller_web/main.js`
- **US_0005_FI_0003:** Completion feedback
  - How: UI/log notifications when done
  - Who: Software Engineer / `src/web_server.py`

### Acceptance Criteria (BDD scenarios)
- **US_0005_AC_0001:** At least two preset patterns execute to completion within documented durations.
- **US_0005_AC_0002:** Completion feedback provided via UI or logs.
- **US_0005_AC_0003:** Presets interruptible by manual controls.

### Traceability
- Related requirements: `FR_008` (Preset Motions)
- Related user story items: US_0005_FI_0001..0003
- Links back: See `documentation/requirements.md` for FR_008 details.

### Testing Strategy
- **Test Types:** Unit, Integration
- **Unit tests:**
  - `tests/test_rasptank_control.py` — test motion sequences
- **Coverage Goals:** ≥70% for preset logic.
- **Test Approach per AC:**
  - AC_0001 (execution): unit tests for sequences; timing verification.
  - AC_0002 (feedback): integration tests for notifications.
  - AC_0003 (interrupt): tests for manual override.

### Code modules
- Implementation: `src/rasptank_controls.py`, `controller_web/main.js`
- Tests: `tests/test_rasptank_control.py`

### Design artifacts to produce
- Motion pattern flowcharts

### Design Artifacts

#### Motion Pattern Flowcharts
*Placeholder: Flowcharts for preset motion patterns (e.g., square, figure-eight).*

### Implementation tasks (backlog suggestions)
- **T1:** Implement motion patterns (US_0005_FI_0001) — Priority: Medium, Effort: 2 days, Status: Pending
- **T2:** Add UI controls (US_0005_FI_0002) — Priority: Low, Effort: 1 day, Status: Pending
- **T3:** Add feedback (US_0005_FI_0003) — Priority: Low, Effort: 0.5 days, Status: Pending

### Last Updated
October 12, 2025
