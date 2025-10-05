#!/usr/bin/python3
# File name   : Ultrasonic.py
# Description : Detection distance and tracking with ultrasonic
# Website     : www.gewbot.com
# Author      : Adeept
# Date        : 2019/08/28
import builtins as _builtins  # keep as module to allow tests to patch builtins.open
import subprocess
import shutil
import psutil


def _read_cpu_temp_str(path: str = "/sys/class/thermal/thermal_zone0/temp") -> str:
    """Read CPU temperature from sysfs and return a string rounded to 0.1°C.
    Fails if the path does not exist or cannot be read. Tests can mock builtins.open.
    """
    with _builtins.open(path, "r", encoding="utf-8") as mytmpfile:
        last_line = "0"
        for line in mytmpfile:
            last_line = line
    cpu_temp = float(last_line) / 1000.0
    return str(round(cpu_temp, 1))


def get_info():
    """Return system info as a list of strings: [cpu_temp, cpu_use, ram_use].
    Fail if the CPU temperature path does not exist or cannot be read.
    Tests can mock builtins.open to avoid filesystem dependencies.
    """
    return [get_cpu_tempfunc(), get_cpu_use(), get_ram_info()]


def get_cpu_tempfunc():  # pragma: no cover
    """Return CPU temperature"""
    return _read_cpu_temp_str()


def get_gpu_tempfunc():  # pragma: no cover
    """Return GPU temperature as a character string using vcgencmd.
    Uses subprocess for robustness; errors propagate if the command is missing/fails.
    """
    cmd = shutil.which("vcgencmd") or "/opt/vc/bin/vcgencmd"
    result = subprocess.run(
        [cmd, "measure_temp"], check=True, capture_output=True, text=True
    )
    res = result.stdout.splitlines()[0] if result.stdout else ""
    return res.replace("temp=", "")


def get_cpu_use():
    """Return CPU usage using psutil"""
    cpu_cent = psutil.cpu_percent()
    return str(cpu_cent)


def get_ram_info():
    """Return RAM usage using psutil"""
    ram_cent = psutil.virtual_memory()[2]
    return str(ram_cent)


def get_swap_info():  # pragma: no cover
    """Return swap memory  usage using psutil"""
    swap_cent = psutil.swap_memory()[3]
    return str(swap_cent)
