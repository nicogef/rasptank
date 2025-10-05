from unittest.mock import patch, mock_open, call
from src import system

def iterable_mock_open(read_data):
    m = mock_open(read_data=read_data)
    m.return_value.__iter__.return_value = read_data.splitlines(True)
    return m

with patch('builtins.open', new_callable=iterable_mock_open, read_data="45000\n") as m:
    info = system.get_info()
    print('INFO:', info)
    print('CALLS:', m.call_args_list)
    print('EQUALS EXPECTED:', call("/sys/class/thermal/thermal_zone0/temp", "r") in m.call_args_list)
