import threading

# Define LED types and their color order offsets
# LED_TYPES = {
#    'RGB': 0x06,  # 0b00000110 -> R=0,G=1,B=2
#    'RBG': 0x09,  # 0b00001001 -> R=0,B=1,G=2
#    'GRB': 0x12,  # 0b00010010 -> G=0,R=1,B=2
#    'GBR': 0x21,  # 0b00100001 -> G=0,B=1,R=2
#    'BRG': 0x18,  # 0b00011000 -> B=0,R=1,G=2
#    'BGR': 0x24  # 0b00100100 -> B=0,G=1,R=2
# }
PREDEFINED_COLORS = {
    "black": (0, 0, 0),
    "red": (255, 0, 0),
    "orange": (255, 127, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "indigo": (75, 0, 130),
    "violet": (148, 0, 211),
    "white": (255, 255, 255),
}


class LedCtrl(threading.Thread):
    def __init__(
        self,
        spi,
        *,
        count=8,
        default_brightness=255,
        sequence="GRB",
        default_color=PREDEFINED_COLORS["black"],
    ):

        # validate spi state
        if not spi or not spi.is_open:
            raise ValueError("SPI is not initialized. Please initialize SPI first.")
        self.spi = spi

        # initialize LED state
        self.led_red_offset = sequence.find("R")
        self.led_green_offset = sequence.find("G")
        self.led_blue_offset = sequence.find("B")
        if (
            self.led_red_offset < 0
            or self.led_green_offset < 0
            or self.led_blue_offset < 0
        ):
            raise ValueError(
                f"{sequence} is an invalid a permutation of 'R', 'G', 'B'."
            )
        self.led_count = count
        self.default_color = default_color
        self.default_brightness = default_brightness
        self.led_color = self.default_color * self.led_count
        self.led_brightness = [self.default_brightness] * self.led_count

        # Init Complete show leds
        self.show()

        # initialize Thread
        super().__init__()
        self.__flag = threading.Event()
        self.__flag.clear()
        self.start()

    def set_all_led_brightness(self, brightness):
        self.led_brightness = [brightness] * self.led_count
        self.show()

    def set_all_led_rgb(self, color):
        if len(color) != 3:
            raise ValueError(
                "Color must be a list of three integers representing RGB values."
            )
        self.led_color = color * self.led_count
        self.show()

    def reset(self):
        self.led_brightness = [self.default_brightness] * self.led_count
        self.led_color = self.default_color * self.led_count
        self.show()

    def set_one_led_color(self, led, color):
        self.led_color[led * 3 + self.led_red_offset] = color[0]
        self.led_color[led * 3 + self.led_green_offset] = color[1]
        self.led_color[led * 3 + self.led_blue_offset] = color[2]

    def set_one_led_brightness(self, led, brightness):
        self.led_brightness[led] = brightness

    def show(self):
        led_command = [
            round(color * (self.led_brightness[led // 3] / 255))
            for led, color in enumerate(self.led_color)
        ]
        self.spi.write(led_command)

    def stop(self):
        self.reset()
        self.spi.close()

    ##################################
    ####### Thread Management ########
    ##################################
    def resume(self):
        # self.__flag.set()
        pass

    def pause(self):
        self.set_all_led_rgb([0, 0, 0])
        self.__flag.clear()

    def run(self):
        while 1:
            self.__flag.wait()
            # self.lightChange()
