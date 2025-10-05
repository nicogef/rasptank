#!/usr/bin/env/python
# File name   : server.py
# Production  : picar-b
# Website     : www.adeept.com
# Author      : devin

import time
import threading
import os

#websocket
import asyncio
import websockets

import json
import app
import socket

from src import system as _system
from src.hardware.pca9685_controller import PCA9685Controller
from src.hardware.spi_controller import SpiController
from src.controllers.servo import ServoCtrlThread
from src.controllers.motors import Movement
from src.controllers.leds import LedCtrl, PREDEFINED_COLORS

OLED_connection = 0

functionMode = 0
rad = 0.5
turnWiggle = 60

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
    'armUp':     ARM.clockwise,
    'armDown':   ARM.anticlockwise,
    'armStop':   ARM.stop,
    'handUp':    HAND.clockwise,
    'handDown':  HAND.anticlockwise,
    'handStop':  HAND.stop,
    'lookleft':  WRIST.clockwise,
    'lookright': WRIST.anticlockwise,
    'LRstop':    WRIST.stop,
    'grab':      CLAW.clockwise,
    'loose':     CLAW.anticlockwise,
    'GLstop':    CLAW.stop,
    'up':        CAMERA.clockwise,
    'down':      CAMERA.anticlockwise,
    'UDstop':    CAMERA.stop,
    'home': lambda: servoPosInit(),
    # Motors
    'forward':    MOVEMENT.forward,
    'backward':   MOVEMENT.backward,
    'left':       MOVEMENT.left,
    'right':      MOVEMENT.right,
    'DS':         MOVEMENT.stop,
    'TS':         MOVEMENT.stop,
    'get_info':   system.get_info,
}

controls_with_1_args = {
    'wsB':           MOVEMENT.set_speed,
}

def servoPosInit():
    ARM.reset()
    HAND.reset()
    WRIST.reset()
    CAMERA.reset()
    CLAW.reset()


def ap_thread():  # pragma: no cover
    os.system("sudo create_ap wlan0 eth0 Adeept_Robot 12345678")
            
def wifi_check():
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        s.connect(("1.1.1.1",80))
        ipaddr_check=s.getsockname()[0]
        s.close()
        print(ipaddr_check)
    except Exception:
        ap_threading = threading.Thread(target=ap_thread)
        ap_threading.setDaemon(daemonic=True)
        ap_threading.start()
        time.sleep(1)

def success(command, result):
    return {
        'status': 'ok',
        'title': command,
        'data': result
    }

def failed(command, result):
    return {
        'status': 'nok',
        'title': command,
        'data': result
    }


async def check_permit(websocket):
    while True:
        recv_str = await websocket.recv()
        cred_dict = recv_str.split(":")
        if cred_dict[0] == "admin" and cred_dict[1] == "123456":
            response_str = "congratulation, you have connect with server\r\nnow, you can do something else"
            await websocket.send(response_str)
            return True
        else:
            response_str = "sorry, the username or password is wrong, please submit again"
            await websocket.send(response_str)

async def recv_msg(websocket):

    def _exec_single(command_str: str):
        # Helper to execute one command string and return a response dict
        cmd = command_str.split()[0]
        try:
            value = int(command_str.split()[1]) if len(command_str.split()) > 1 else None
        except Exception:
            value = None
        if cmd in controls:
            controls[cmd]()
            return success(cmd, f"Command {cmd} Executed")
        elif cmd in controls_with_1_args:
            if value is not None:
                controls_with_1_args[cmd](value)
                return success(cmd, f"Command {cmd} Executed")
            else:
                return failed(cmd, f"Command {cmd} Need 1 argument")
        else:
            return failed(cmd, f"Command {cmd} Not Supported")

    while True: 
        response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

        data = await websocket.recv()
        try:
            data = json.loads(data)
        except Exception as ex:
            print(ex)

        if data is None or (isinstance(data, str) and not data.strip()):
            print("No data received")
            continue

        print(data)
        # Support multiple tasks in parallel when receiving a list of commands
        if isinstance(data, list):
            loop = asyncio.get_running_loop()
            tasks = [loop.run_in_executor(None, _exec_single, str(item)) for item in data]
            results = await asyncio.gather(*tasks, return_exceptions=False)
            await websocket.send(json.dumps(results))
            continue

        if isinstance(data, str):
            command = data.split()[0]
            value = int(data.split()[1]) if len(data.split()) > 1 else None
            if command in controls:
                controls[command]()
                response = success(command, f"Command {command} Executed")
            elif command in controls_with_1_args:
                if value is not None:
                    controls_with_1_args[command](value)
                    response = success(command, f"Command {command} Executed")
                else:
                    response = failed(command, f"Command {command} Need 1 argument")
            else:
                response = failed(command, f"Command {command} Not Supported")
        else:
            response = failed('unknown', f"Command Not Supported: {data}")
        json_dumps = json.dumps(response)
        await websocket.send(json_dumps)

async def main_logic(websocket, path):
    await check_permit(websocket)
    await recv_msg(websocket)

if __name__ == '__main__':  # pragma: no cover

    HOST = ''
    PORT = 10223                              #Define port serial 
    BUFSIZ = 1024                             #Define buffer size
    ADDR = (HOST, PORT)

    global flask_app
    flask_app = app.webapp()
    flask_app.startthread()
    try:
        LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS['orange'])
        while  1:
            wifi_check()
            try:                  #Start server,waiting for client
                start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
                asyncio.get_event_loop().run_until_complete(start_server)
                print('waiting for connection...')
                break
            except Exception as e:
                LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS['red'])
                print('connection error...')
                raise e
                
                
        LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS['green'])
        print('start main loop...')
        try:
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            print(e)
            LED_CTRL.set_all_led_rgb(PREDEFINED_COLORS['red'])
            MOVEMENT.stop()
    except KeyboardInterrupt:
        print('program stopped...')
        MOVEMENT.stop()
        LED_CTRL.stop()
        exit(0)
