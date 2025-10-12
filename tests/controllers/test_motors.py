import unittest
from unittest.mock import MagicMock

from src.controllers.motors import Movement, FORWARD


class SimpleMotor:
    def __init__(self):
        self.throttle = None

    def __repr__(self):
        return f"<SimpleMotor throttle={self.throttle}>"


class TestMovement(unittest.TestCase):
    def setUp(self):
        # construct controller that returns SimpleMotor instances
        self.motor1 = SimpleMotor()
        self.motor2 = SimpleMotor()
        controller = MagicMock()
        controller.motor = lambda idx: self.motor1 if idx == 1 else self.motor2
        # motor1_direction and motor2_direction simulate wiring/polarity
        # Set speed to 70 to match the expected test values
        self.movement = Movement(controller, motor1_direction=FORWARD, motor2_direction=FORWARD, speed=70)

    def test_forward_sets_throttles_positive(self):
        self.movement.forward()
        self.assertEqual(self.motor1.throttle, 70)
        self.assertEqual(self.motor2.throttle, 70)

    def test_backward_sets_throttles_negative(self):
        self.movement.backward()
        self.assertEqual(self.motor1.throttle, -70)
        self.assertEqual(self.motor2.throttle, -70)

    def test_left_differential_steering(self):
        self.movement.left()
        self.assertEqual(self.motor1.throttle, 70)
        self.assertEqual(self.motor2.throttle, -70)

    def test_right_differential_steering(self):
        self.movement.right()
        self.assertEqual(self.motor1.throttle, -70)
        self.assertEqual(self.motor2.throttle, 70)

    def test_stop_zeros_throttles(self):
        self.movement.forward()
        self.movement.stop()
        self.assertEqual(self.motor1.throttle, 0)
        self.assertEqual(self.motor2.throttle, 0)

    def test_set_speed_changes_throttle_magnitude(self):
        self.movement.set_speed(90)
        self.movement.forward()
        expected = 90  # 90% throttle
        self.assertEqual(self.motor1.throttle, expected)
        self.assertEqual(self.motor2.throttle, expected)


if __name__ == "__main__":
    unittest.main()
