import spidev  # pylint: disable=import-error
import numpy


class SpiController:
    def __init__(self, bus=0, device=0, mode=1):
        self.bus = bus
        self.device = device
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(self.bus, self.device)
            self.spi.mode = 0
            self.write = self.write_ws2812_numpy8 if mode == 1 else self.write_ws2812_numpy4
        except OSError:
            print("Please check the configuration in /boot/firmware/config.txt.")
            if self.bus == 0:
                print("You can turn on the 'SPI' in 'Interface Options' by using 'sudo raspi-config'.")
                print(
                    "Or make sure that 'dtparam=spi=on' is not commented, then reboot the Raspberry Pi. "
                    "Otherwise spi0 will not be available."
                )
            else:
                print(
                    f"Please add 'dtoverlay=spi{self.bus}-2cs' at the bottom of the /boot/firmware/config.txt, "
                    f"then reboot the Raspberry Pi. otherwise spi{self.bus} will not be available."
                )
            self.close()
            raise

    def close(self):
        self.spi.close()

    def write_ws2812_numpy8(self, led_color):
        data = numpy.array(led_color).ravel()  # Converts data into a one-dimensional array
        tx_bytes = numpy.zeros(
            len(data) * 8, dtype=numpy.uint8
        )  # Each RGB color has 8 bits, each represented by a uint8 type data
        for ibit in range(8):
            # Convert each bit of data to the data that the spi will send
            # T0H=1,T0L=7 - T1H=5,T1L=3
            # -> #0b11111000 mean T1(0.78125us), 0b10000000 mean T0(0.15625us)
            tx_bytes[7 - ibit :: 8] = ((data >> ibit) & 1) * 0x78 + 0x80
        if self.bus == 0:
            self.spi.xfer(tx_bytes.tolist(), int(8 / 1.25e-6))  # Send color data at a frequency of 6.4Mhz
        else:
            self.spi.xfer(tx_bytes.tolist(), int(8 / 1.0e-6))  # Send color data at a frequency of 8Mhz

    def write_ws2812_numpy4(self, led_color):
        data = numpy.array(led_color).ravel()
        tx_bytes = numpy.zeros(len(data) * 4, dtype=numpy.uint8)
        for ibit in range(4):
            tx_bytes[3 - ibit :: 4] = ((data >> (2 * ibit + 1)) & 1) * 0x60 + ((data >> (2 * ibit + 0)) & 1) * 0x06 + 0x88
        if self.bus == 0:
            self.spi.xfer(tx_bytes.tolist(), int(4 / 1.25e-6))
        else:
            self.spi.xfer(tx_bytes.tolist(), int(4 / 1.0e-6))
