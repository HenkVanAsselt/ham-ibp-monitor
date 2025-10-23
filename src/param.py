"""File for global variables
"""

import serial  # type: ignore

port: serial.Serial | None = None

mode_dict = {
    '1': 'LSB',
    '2': 'USB',
    '3': 'CW-U',
    '4': 'FM',
    '5': 'AM',
    '6': 'RTTY-L',
    '7': 'CW-L',
    '8': 'DATA-L',
    '9': 'RTTY-U',
    'A': 'DATA-FM',
    'B': 'FM-N',
    'C': 'DATA-U',
    'D': 'AM-N', 
    'E': 'PSK',
    'F': 'DATA-FM-N'
}

str_to_mode_dict = {v: k for k, v in mode_dict.items()}

beacon_frequency = {
    14: 14.100,  # 20 meter = 14 MHz
    18: 18.110,  # 17 meter = 18 MHz
    21: 21.150,  # 15 meter = 21 MHz
    24: 24.930,  # 12 meter = 24 MHz
    28: 28.200,  # 10 meter = 28 MHz
}


