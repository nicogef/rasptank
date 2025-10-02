import unittest
from unittest.mock import MagicMock

from tests import async_helper
from src.controllers.servo import ServoCtrlThread, ANTICLOCKWISE


class FakeServo:
    def __init__(self):
        self.angle = None


class TestServoCtrlThread(unittest.TestCase):
    def setUp(self):

        # prepare fake controller with servo(channel) factory
        self.fake_servo = FakeServo()
        controller = MagicMock()
        controller.servo = lambda ch: self.fake_servo

        # instantiate while thread start is patched
        self.svc = ServoCtrlThread("test", controller, 0, 90)

    def tearDown(self):
        if self.svc.is_alive():
            self.svc.stop_thread()

    def test_initial_angle_set(self):
        self.svc.reset()
        self.assertEqual(90, int(round(self.svc.angle_current_value)))
        self.assertEqual(90, self.fake_servo.angle)

    def test_reset(self):
        self.assertEqual(90, self.svc.angle_initial_value)
        self.assertEqual(90, int(round(self.svc.angle_current_value)))
        self.assertEqual(90, self.fake_servo.angle)

    def test_set_angle_within_range(self):
        # call the name-mangled private method
        self.svc.move_to(120)
        async_helper.wait_for(lambda: self.assert_angle_reached(120))

    def test_set_angle_clips_to_max(self):
        # set beyond maximum -> clipped to angle_maximum_range (180)
        self.svc.move_to(200)
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_maximum_range)
        )

    def test_set_angle_stops(self):
        self.svc.move_to(180)
        self.svc.stop()
        async_helper.wait_for(lambda: self.assert_angle_not_reached(180))

    def test_set_angle_clips_to_min(self):
        self.svc.move_to(-15)
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_minimum_range)
        )

    def test_increment_and_decrement_pwm(self):
        # start from 90 by default
        self.svc.increment_pwm()
        self.assertEqual(91, self.fake_servo.angle)
        self.svc.increment_pwm()
        self.assertEqual(92, self.fake_servo.angle)
        self.svc.derement_pwm()
        self.assertEqual(91, self.fake_servo.angle)

    def test_clockwise(self):
        self.svc.clockwise()
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_maximum_range)
        )

    def test_anticlockwise(self):
        self.svc.anticlockwise()
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_minimum_range)
        )

    def test_move_by_number_of_steps(self):
        expected_angle = self.svc.angle_current_value + 10
        self.svc.move(number_of_steps=10)
        async_helper.wait_for(lambda: self.assert_angle_reached(expected_angle))

    def test_clockwise_reversed_direction(self):
        self.svc.servo_direction = ANTICLOCKWISE
        self.svc.clockwise()
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_minimum_range)
        )

    def test_anticlockwise_reversed_direction(self):
        # set beyond maximum -> clipped to angle_maximum_range (180)
        self.svc.servo_direction = ANTICLOCKWISE
        self.svc.anticlockwise()
        async_helper.wait_for(
            lambda: self.assert_angle_reached(self.svc.angle_maximum_range)
        )

    def assert_angle_reached(self, expected):
        try:
            self.assertEqual(
                False,
                self.svc._ServoCtrlThread__flag.is_set(),  # pylint: disable=protected-access
            )
            self.assertEqual(expected, self.svc.angle_current_value)
            self.assertEqual(expected, self.fake_servo.angle)
            return True
        except AssertionError:
            return False

    def assert_angle_not_reached(self, not_expected):
        try:
            self.assertEqual(
                False,
                self.svc._ServoCtrlThread__flag.is_set(),  # pylint: disable=protected-access
            )
            self.assertNotEqual(not_expected, self.svc.angle_current_value)
            self.assertNotEqual(not_expected, self.fake_servo.angle)
            return True
        except AssertionError:
            return False


if __name__ == "__main__":
    unittest.main()
