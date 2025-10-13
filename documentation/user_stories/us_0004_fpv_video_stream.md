# US_0004: FPV Video Stream

**ID:** US_0004

**Title:** FPV Video Stream

**What & Why:**
As an End User, I want to view live camera video with adjustable quality, so that I can monitor the robot's environment in real-time.

### Feature Items (How & Who)
- **US_0004_FI_0001:** Video streaming setup
  - How: Camera capture and network streaming with resolution/FPS controls
  - Who: Software Engineer / `src/web_server.py`, `web/*`
- **US_0004_FI_0002:** Web UI video display
  - How: Embedded video player with controls
  - Who: Web Developer / `controller_web/index.html`
- **US_0004_FI_0003:** Adjustable quality settings
  - How: Configurable resolution and frame rate
  - Who: Software Engineer / `src/web_server.py`

### Acceptance Criteria (BDD scenarios)
- **US_0004_AC_0001:** Stream starts within 3 seconds of accessing video view.
- **US_0004_AC_0002:** Default quality ≥ 640×480 at 20 FPS on Pi 4.
- **US_0004_AC_0003:** Resolution and FPS adjustable via UI or config.
- **US_0004_AC_0004:** Video accessible on supported browsers.

### Traceability
- Related requirements: `FR_004` (FPV Video Stream), `NFR_003` (Performance)
- Related user story items: US_0004_FI_0001..0003
- Links back: See `documentation/requirements.md` for FR_004 details.

### Testing Strategy
- **Test Types:** Integration, E2E, Performance
- **Integration/E2E tests:**
  - `tests/test_webpage_with_mock.py` — video stream loading
- **Coverage Goals:** Achieve ≥70% code coverage for video-related modules.
- **Test Approach per AC:**
  - AC_0001 (startup): measure load time; integration tests.
  - AC_0002 (quality): performance tests for FPS/resolution.
  - AC_0003 (adjustable): UI tests for settings.
  - AC_0004 (browsers): cross-browser E2E tests.

### Code modules
- Implementation: `src/web_server.py`, `web/*`, `controller_web/index.html`
- Tests: `tests/test_webpage_with_mock.py`, `tests/test_webpage_clicks_e2e.py`

### Design artifacts to produce
- Video streaming architecture diagram

### Design Artifacts

#### Video Streaming Architecture Diagram
This diagram shows the architecture for capturing and streaming video.

```plantuml
@startuml
title Video Streaming Architecture

package "web" {
    class BaseCamera {
        +thread: Thread
        +frame: bytes
        +event: CameraEvent
        +get_frame(): bytes
        +{static}_thread()
    }

    class CameraEvent {
        +events: dict
        +wait()
        +set()
        +clear()
    }

    class Camera(BaseCamera) {
        +{static}frames()
    }

    class CVThread {
        +run()
        +mode()
        +elementDraw()
    }
}

package "picamera2" {
    class Picamera2
}

actor "Client" as Client
participant "Flask App (app.py)" as FlaskApp

Client -> FlaskApp: GET /video_feed
FlaskApp -> Camera: get_frame()
Camera -> BaseCamera: get_frame()
BaseCamera -> CameraEvent: wait()

note right of BaseCamera
  The _thread in BaseCamera runs in the background,
  continuously getting frames from the Camera.frames() generator.
end note

Camera.frames() -> Picamera2: capture_array()
Picamera2 --> Camera.frames(): returns frame
Camera.frames() -> CVThread: mode(mode, frame)
CVThread -> CVThread: Processes frame
CVThread --> Camera.frames(): returns processed frame
Camera.frames() --> BaseCamera._thread: yields frame

BaseCamera._thread -> BaseCamera: frame = new_frame
BaseCamera._thread -> CameraEvent: set()

CameraEvent --> BaseCamera: Event is set
BaseCamera --> FlaskApp: returns frame
FlaskApp --> Client: Responds with MJPEG frame
@enduml
```

*Note: The video stream is managed by a multi-threaded system. A background thread in `BaseCamera` continuously captures frames from the `Picamera2` library via the `Camera.frames()` generator. An optional `CVThread` can process these frames. A `CameraEvent` object synchronizes access, ensuring that the Flask web server can efficiently retrieve and stream the latest frame to the client as an MJPEG feed.*

### Implementation tasks (backlog suggestions)
- **T1:** Set up video streaming (US_0004_FI_0001) — Priority: High, Effort: 3-4 days, Status: Pending
- **T2:** Integrate web UI video player (US_0004_FI_0002) — Priority: Medium, Effort: 2 days, Status: Pending
- **T3:** Add quality controls (US_0004_FI_0003) — Priority: Low, Effort: 1 day, Status: Pending

### Last Updated
October 12, 2025
