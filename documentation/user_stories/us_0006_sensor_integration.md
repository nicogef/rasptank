# US_0006: Sensor Integration

**ID:** US_0006

**Title:** Sensor Integration

**What & Why:**
As an End User, I want access to ultrasonic sensor readings, so that I can detect obstacles and enhance navigation.

### Feature Items (How & Who)
- **US_0006_FI_0001:** Sensor data reading
  - How: Periodic ultrasonic measurements
  - Who: Robotics Engineer / `src/controllers/ultra.py` or similar
- **US_0006_FI_0002:** API/UI exposure
  - How: Expose readings via WebSocket/API
  - Who: Software Engineer / `src/web_server.py`
- **US_0006_FI_0003:** Error handling for unavailable sensors
  - How: Graceful degradation with unavailable status
  - Who: Software Engineer / `src/system.py`

### Acceptance Criteria (BDD scenarios)
- **US_0006_AC_0001:** Distance values update at least every 100 ms when sensor present.
- **US_0006_AC_0002:** Readings unavailable when sensor fails, without crashes.
- **US_0006_AC_0003:** API endpoint documented and stable.

### Traceability
- Related requirements: `FR_005` (Sensor Integration)
- Related user story items: US_0006_FI_0001..0003
- Links back: See `documentation/requirements.md` for FR_005 details.

### Testing Strategy
- **Test Types:** Unit, Integration
- **Unit tests:**
  - `tests/test_system.py` — sensor data handling
- **Coverage Goals:** ≥70% for sensor modules.
- **Test Approach per AC:**
  - AC_0001 (updates): timing tests for data refresh.
  - AC_0002 (error handling): fault injection tests.
  - AC_0003 (API): integration tests for endpoints.

### Code modules
- Implementation: `web/ultra.py`, `src/web_server.py`, `src/system.py`
- Tests: `tests/test_system.py`, `tests/test_webpage_with_mock.py`

### Design artifacts to produce
- Sensor data flow diagram

### Design Artifacts

#### Sensor Data Flow Diagram
This diagram shows how the ultrasonic sensor data is read and used.

```plantuml
@startuml
title Sensor Data Flow

package "web" {
    participant "ultra.py" as Ultra
}

package "gpiozero" {
    participant "DistanceSensor" as GpioSensor
}

participant "Application Logic" as AppLogic

AppLogic -> Ultra: checkdist()
Ultra -> GpioSensor: sensor.distance
GpioSensor --> Ultra: returns distance
Ultra --> AppLogic: returns distance in cm

@enduml
```

*Note: The `ultra.py` module provides a simple `checkdist()` function that reads the distance from a `gpiozero.DistanceSensor` instance. This function is then called by other parts of the application, such as the preset motion logic in `web/functions.py`, to get obstacle information.*

### Implementation tasks (backlog suggestions)
- **T1:** Implement sensor reading (US_0006_FI_0001) — Priority: Medium, Effort: 2 days, Status: Pending
- **T2:** Expose via API/UI (US_0006_FI_0002) — Priority: Medium, Effort: 1 day, Status: Pending
- **T3:** Add error handling (US_0006_FI_0003) — Priority: Low, Effort: 1 day, Status: Pending

### Last Updated
October 12, 2025
