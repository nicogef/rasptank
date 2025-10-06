import unittest

from src.controllers.leds import LedCtrl, PREDEFINED_COLORS


class SpiMock:
    def __init__(self, is_open=True):
        self.is_open = is_open
        self.writes = []
        self.closed = False

    def write(self, data):
        # store a copy to avoid mutation surprises
        self.writes.append(list(data))

    def close(self):
        self.closed = True


class TestLedCtrl(unittest.TestCase):
    def test_requires_open_spi(self):
        spi = SpiMock(is_open=False)
        with self.assertRaises(ValueError):
            LedCtrl(spi)

    def test_invalid_sequence_raises(self):
        spi = SpiMock()
        with self.assertRaises(ValueError):
            LedCtrl(spi, sequence="RXB")

    def test_set_all_led_rgb_and_brightness(self):
        spi = SpiMock()
        ctrl = LedCtrl(spi, count=2, sequence="RGB")
        # First write happens in __init__ with default black
        self.assertEqual(spi.writes[0], [0] * 6)

        # Set color for all leds
        ctrl.set_all_led_rgb((10, 20, 30))
        # Expect two LEDs -> 6 values
        self.assertEqual(spi.writes[-1], [10, 20, 30, 10, 20, 30])

        # Now dim to ~50% (128/255)
        ctrl.set_all_led_brightness(128)
        scale = 128 / 255
        expected = [round(v * scale) for v in [10, 20, 30, 10, 20, 30]]
        self.assertEqual(spi.writes[-1], expected)

        # Pause should turn off (send zeros)
        ctrl.pause()
        self.assertEqual(spi.writes[-1], [0, 0, 0, 0, 0, 0])

        # Stop should reset (zeros) and close SPI
        ctrl.stop()
        self.assertTrue(spi.closed)

    def test_per_led_color_and_brightness_mapping(self):
        spi = SpiMock()
        ctrl = LedCtrl(spi, count=3, sequence="RGB", default_color=PREDEFINED_COLORS["black"])

        # set LED0 -> (100, 0, 0), LED1 -> (0, 50, 0), LED2 -> (0, 0, 200)
        ctrl.set_one_led_color(0, (100, 0, 0))
        ctrl.set_one_led_color(1, (0, 50, 0))
        ctrl.set_one_led_color(2, (0, 0, 200))
        # different brightness per LED
        ctrl.set_one_led_brightness(0, 255)
        ctrl.set_one_led_brightness(1, 128)
        ctrl.set_one_led_brightness(2, 64)
        ctrl.show()

        # Build expected command list considering brightness scaling
        def scale(vals, b):
            return [round(x * (b / 255)) for x in vals]

        expected = []
        expected += scale([100, 0, 0], 255)
        expected += scale([0, 50, 0], 128)
        expected += scale([0, 0, 200], 64)

        self.assertEqual(spi.writes[-1], expected)


if __name__ == "__main__":
    unittest.main()
