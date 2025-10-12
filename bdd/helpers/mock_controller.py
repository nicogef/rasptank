class MockController:
    """Lightweight mock controller used by BDD step definitions.

    - map_speed: maps normalized speed (0.0-1.0) to motor units (0-100)
    - process_command: simulates processing, clamping and motor-start timestamp
    """

    def __init__(self, max_speed=1.0):
        self.max_speed = max_speed
        self.last_clamped = False

    def map_speed(self, speed: float) -> float:
        clamped_speed = max(0.0, min(1.0, float(speed)))
        return clamped_speed * 100.0

    def process_command(self, direction: str, speed: float, cmd_ts: float):
        self.last_clamped = False
        cmd_speed = float(speed)
        if cmd_speed > self.max_speed:
            cmd_speed = self.max_speed
            self.last_clamped = True
        motor_output = self.map_speed(cmd_speed)
        # Simulate a small processing delay (20 ms) for motor start
        motor_start_ts = cmd_ts + 0.02
        # Return a dict compatible with step defs
        return {
            "direction": direction,
            "cmd_ts": cmd_ts,
            "motor_start_ts": motor_start_ts,
            "motor_output": motor_output,
            "cmd_speed": cmd_speed,
        }
