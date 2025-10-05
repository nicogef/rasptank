from unittest.mock import patch, mock_open, call
from src import system


def iterable_mock_open(read_data):
    mocked_open = mock_open(read_data=read_data)
    mocked_open.return_value.__iter__.return_value = read_data.splitlines(True)
    return mocked_open


with patch(
    "builtins.open", new_callable=iterable_mock_open, read_data="45000\n"
) as mocked_file:
    info = system.get_info()
    print("INFO:", info)
    print("CALLS:", mocked_file.call_args_list)
    print(
        "EQUALS EXPECTED:",
        call("/sys/class/thermal/thermal_zone0/temp", "r")
        in mocked_file.call_args_list,
    )
