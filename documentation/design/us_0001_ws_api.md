# US_0001 WebSocket API Schema

This document describes the WebSocket message schema for drive commands in US_0001.

## Message Format
- **Type:** JSON
- **Direction:** Client → Server
- **Fields:**
  - `command`: String (e.g., "forward", "stop")
  - `speed`: Float (0.0 to 1.0)
  - `timestamp`: Integer (Unix timestamp in milliseconds)

## Example
```json
{
  "command": "forward",
  "speed": 0.8,
  "timestamp": 1699999999999
}
```

## Response
Server acknowledges with:
```json
{
  "status": "ok",
  "timestamp": 1699999999999
}
```

*Note: This is a placeholder. Replace with actual diagram and details.*

