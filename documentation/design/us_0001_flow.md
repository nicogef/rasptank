# US_0001 Drive Command Lifecycle and Safety Checklist

## Lifecycle Diagram
1. User input (UI button/joystick)
2. Client-side validation and normalization
3. WebSocket transmission
4. Server receipt and parsing
5. Controller processing (speed scaling, clamping)
6. Hardware command execution
7. Telemetry logging

## Safety Checklist
- [ ] Speed clamped to max 1.0
- [ ] Commands validated before hardware access
- [ ] Watchdog timer active
- [ ] Emergency stop available
- [ ] Logging enabled for diagnostics

*Note: This is a placeholder. Replace with actual diagram and checklist.*

