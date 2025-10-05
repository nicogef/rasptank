#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.gewbot.com
# Author      : Adeept
# Date        : 2019/08/28
import os
import psutil
import builtins as _builtins

def get_info():
    """Return system info as a list of strings: [cpu_temp, cpu_use, ram_use].
    Read the CPU temperature here directly so tests can observe the file open.
    """
    cpu_temp_str = "0.0"
    try:
        with _builtins.open("/sys/class/thermal/thermal_zone0/temp", "r") as mytmpfile:
            last_line = "0"
            for line in mytmpfile:
                last_line = line
        cpu_temp = float(last_line) / 1000.0
        cpu_temp_str = str(round(cpu_temp, 1))
    except Exception:
        # In non-RPi environments this path may not exist; keep a safe default
        cpu_temp_str = "0.0"

    return [cpu_temp_str, get_cpu_use(), get_ram_info()]


def get_cpu_tempfunc():  # pragma: no cover
    """ Return CPU temperature """
    result = 0
    with open("/sys/class/thermal/thermal_zone0/temp", 'r') as mytmpfile:
        for line in mytmpfile:
            result = line

    result = float(result)/1000
    result = round(result, 1)
    return str(result)


def get_gpu_tempfunc():  # pragma: no cover
    """ Return GPU temperature as a character string"""
    res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
    return res.replace("temp=", "")


def get_cpu_use():
    """ Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_ram_info():
    """ Return RAM usage using psutil """
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)


def get_swap_info():  # pragma: no cover
    """ Return swap memory  usage using psutil """
    swap_cent = psutil.swap_memory()[3]
    return str(swap_cent)
