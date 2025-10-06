#!/usr/bin/env/python
# File name   : server.py
# Production  : picar-b
# Website     : www.adeept.com
# Author      : devin

import asyncio
import os
import socket
import sys
import threading
import time

try:  # Optional at runtime; used only when running the websocket server
    import websockets  # type: ignore
except ImportError:  # pragma: no cover - optional dependency not installed in CI/tests
    websockets = None  # type: ignore

try:  # Optional: the web UI app is not required for tests
    import app  # type: ignore
except ImportError:  # pragma: no cover - optional dependency not installed in CI/tests
    app = None  # type: ignore

from src import system as _system
from src.controllers.leds import LedCtrl, PREDEFINED_COLORS
from src.controllers.motors import Movement
from src.controllers.servo import ServoCtrlThread
from src.hardware.pca9685_controller import PCA9685Controller
from src.hardware.spi_controller import SpiController
from src.web_server import WebSocketHandler

OLED_connection = 0  # pylint: disable=invalid-name

functionMode = 0  # pylint: disable=invalid-name
rad = 0.5  # pylint: disable=invalid-name
turnWiggle = 60  # pylint: disable=invalid-name

##################################
####### Servo Controlers  ########
##################################
PCA9685_CTRL = PCA9685Controller()
SPI = SpiController()
ARM = ServoCtrlThread("ARM", PCA9685_CTRL, 0)
HAND = ServoCtrlThread("HAND", PCA9685_CTRL, 1, direction=-1)
WRIST = ServoCtrlThread("WRIST", PCA9685_CTRL, 2)
# 3 is detroyed using 5 instead
CLAW = ServoCtrlThread("CLAW", PCA9685_CTRL, 5)
CAMERA = ServoCtrlThread("CAMERA", PCA9685_CTRL, 4)
SERVOS = [ARM, HAND, WRIST, CLAW, CAMERA]


def servo_pos_init():
    ARM.reset()
    HAND.reset()
    WRIST.reset()
    CAMERA.reset()
    CLAW.reset()


##################################
######## Motor Controler #########
##################################
MOVEMENT = Movement(PCA9685_CTRL, -1, -1)

##################################
######### Led Controler ##########
##################################
LED_CTRL = LedCtrl(SPI)


# Provide a tiny proxy for system to avoid mutating the global src.system in tests
class _SystemProxy:
    def __init__(self, get_info_func):
        self.get_info = get_info_func


system = _SystemProxy(_system.get_info)

controls = {
    # Servos
    "armUp": ARM.clockwise,
    "armDown": ARM.anticlockwise,
    "armStop": ARM.stop,
    "handUp": HAND.clockwise,
    "handDown": HAND.anticlockwise,
    "handStop": HAND.stop,
    "lookleft": WRIST.clockwise,
    "lookright": WRIST.anticlockwise,
    "LRstop": WRIST.stop,
    "grab": CLAW.clockwise,
    "loose": CLAW.anticlockwise,
    "GLstop": CLAW.stop,
    "up": CAMERA.clockwise,
    "down": CAMERA.anticlockwise,
    "UDstop": CAMERA.stop,
    "home": servo_pos_init,
    # Motors
    "forward": MOVEMENT.forward,
    "backward": MOVEMENT.backward,
    "left": MOVEMENT.left,
    "right": MOVEMENT.right,
    "DS": MOVEMENT.stop,
    "TS": MOVEMENT.stop,
    "get_info": system.get_info,
}

controls_with_1_args = {
    "wsB": MOVEMENT.set_speed,
}


def ap_thread():  # pragma: no cover
    os.system("sudo create_ap wlan0 eth0 Adeept_Robot 12345678")


def wifi_check():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ipaddr_check = s.getsockname()[0]
        s.close()
        print(ipaddr_check)
    except Exception:  # pylint: disable=broad-exception-caught
        ap_threading = threading.Thread(target=ap_thread)
        ap_threading.daemon = True  # deprecated setDaemon -> use attribute
        ap_threading.start()
        time.sleep(1)


# Generic dispatcher used by tests and by any legacy callers expecting a single-string command API
if __name__ == "__main__":  # pragma: no cover

    HOST = ""
    PORT = 10223  # Define port serial
    BUFSIZ = 1024  # Define buffer size
    ADDR = (HOST, PORT)

    flask_app = app.webapp()  # type: ignore[attr-defined]
    flask_app.startthread()
    try:
        LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS["orange"])
        while 1:
            wifi_check()
            try:  # Start server,waiting for client
                start_server = websockets.serve(WebSocketHandler(controls, controls_with_1_args), "0.0.0.0", 8888)
                asyncio.get_event_loop().run_until_complete(start_server)
                print("waiting for connection...")
                break
            except Exception as e:
                LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS["red"])
                print("connection error...")
                raise e

        LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS["green"])
        print("start main loop...")
        try:
            asyncio.get_event_loop().run_forever()
        except Exception as e:  # pylint: disable=broad-exception-caught
            print(e)
            LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS["red"])
            MOVEMENT.stop()
    except KeyboardInterrupt:
        print("program stopped...")
        MOVEMENT.stop()
        LED_CTRL.stop()
        sys.exit(0)
