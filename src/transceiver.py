""" Transceiver (Yeasu FTdx10) related functions
"""

# pylint: disable=logging-fstring-interpolation,invalid-name

# Global imports
# import sys
import time
import logging

# 3rd party imports
import serial  # type: ignore

# local imports
from src import param
from src import cat

logging.basicConfig(level=logging.INFO)


def offset_to_str(offset) -> tuple:  # type: ignore
    """ Convert the given offset (int or str) to a string.

    :param offset: Frequency offset (int or str)
    :return: tuple of direction ('+' or '-') and 4-char zero padded string.

    >>> offset_to_str(1502)         # Valid positive offset as an integer
    ('+', '1502')

    >>> offset_to_str(30000)        # Invalid integer of 30 kHz
    ('+', '0000')

    >>> offset_to_str(-5000)        # -5000 as an integer
    ('-', '5000')

    >>> offset_to_str("3000")       # +3000 Hz as a string
    ('+', '3000')

    >>> offset_to_str("-7000")      # -7000 Hz as a string
    ('-', '7000')

    >>> offset_to_str(-50000)       # Invalid negative offset
    ('+', '0000')

    >>> offset_to_str(0)
    ('+', '0000')

    """

    off = "0000"        # Default offset
    direction = '+'     # Default direction

    if isinstance(offset, int):
        if offset > 9999 or offset < -9999:
            logging.error(f"Invalid offset {offset}. Must be between -9999 Hz and +9999 Hz")
            return '+', '0000'
        if offset < 0:
            direction = '-'
            offset = -offset
        off = f"{int(offset):04}"

    if isinstance(offset, str):
        if offset.startswith("+"):
            offset = offset[1:]
        elif offset.startswith('-'):
            direction = '-'
            offset = offset[1:]
        off = f"{int(offset):04}"

    return direction, off


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def show_information() -> None:
    """Get current information from the connected tranceiver


    1  2  3  4  5  6  7  8  9  10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30
    I  F  P1 P1 P1 P2 P2 P2 P2 P2 P2 P2 P2 P2 P3 P3 P3 P3 P3 P4 P5 P6 P7 P8 P9 P9 P10 ;


    0 P 0 0 0 1 - 0 9 9 ( MemoryChannel ) , P1L-P9U ( PMS ) , 5xx ( 5 MHz BAND ) ,
    EMG (EMERGENCY CH)
    P2 VFO-A Frequency (Hz)
    P3	 Clarifier Direction +: Plus Shift, -: Minus Shift
         Clarifier Offset: 0000 - 9990 (Hz)
    P4 0: RX CLAR "OFF" 1: RX CLAR "ON"
    P5 0: TX CLAR "OFF" 1: TX CLAR "O"
    P6 MODE 1: LSB 2: USB 3: CW-U 4: FM 5: AM 6: RTTY-L 7: CW-L
     8: DATA-L 9: RTTY-U A: DATA-FM B: FM-N C: DATA-U
     D: AM-N E: PSK F: DATA-FM-N
    P7 0: VFO 1: Memory 2: Memory Tune 3: Quick Memory Bank (QMB)
    4: - 5: PMS
    P8 0: OFF 1: CTCSS ENC/DEC 2: CTCSS ENC
    P9 00: (Fixed)
    P10 0: Simplex 1: Plus Shift 2: Minus Shift

    Example response:
    IF001007075290+000000100000;

    """

    response = cat.write("IF;")
    # if response:
    #     print(response)

    emergency_channel = response[2:5]
    print(f"{emergency_channel=}")

    frequency = response[5:14]
    print(f"{frequency=}")

    clarifier = response[14:19]
    print(f"{clarifier=}")
    rx_clarifier = response[19]
    print(f"{rx_clarifier=}")
    tx_clarifier = response[20]
    print(f"{tx_clarifier=}")

    mode_int = response[21]
    mode = param.mode_dict.get(mode_int, "Unknown")
    print(f"{mode=}")

    # P7 0: VFO 1: Memory 2: Memory Tune 3: Quick Memory Bank (QMB)
    p7 = response[22]
    tuning_mode = ""
    if p7 == "0":
        tuning_mode = "VFO"
    if p7 == "1":
        tuning_mode = "Memory"
    if p7 == "2":
        tuning_mode = "Memory Tune"
    if p7 == "3":
        tuning_mode = "Quick Memory Bank (QMB)"
    if p7 == "4":
        tuning_mode = "PMS"
    print(f"{tuning_mode=}")

    # P8 0: OFF 1: CTCSS ENC/DEC 2: CTCSS ENC
    p8 = response[23]
    ctcss_mode = ""
    if p8 == "0":
        ctcss_mode = "CTCSS Off"
    if p8 == "1":
        ctcss_mode = "CTCSS ENC/DEC"
    if p8 == "2":
        ctcss_mode = "CTCSS ENC"
    print(f"{ctcss_mode=}")

    p10 = response[25]
    repeater_mode = ""
    # P10 0: Simplex 1: Plus Shift 2: Minus Shift
    if p10 == "0":
        repeater_mode = "Repeater Simplex"
    if p10 == "1":
        repeater_mode = "Repeater Plus Shift"
    if p10 == "2":
        repeater_mode = "Repeater Minus Shift"
    print(f"{repeater_mode=}")


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def set_vfo(frequency: [str | float], vfo: str = "A") -> bool:  # type: ignore
    """Set VFO A to the given frequency

    :param frequency: Frequency to use
    :param vfo: VFO to use ("A" or "B")

    Frequency can be:
    * a string with length 9  (for example "014100000")
    * a float. Assumed to be in MHz. Will be converted to a bytearray and 0 padded
      (for example 14.1)

    :return: True on success, False if an error

    """

    freq_str = "000"

    # If it is a string, convert it to bytes
    if isinstance(frequency, str):
        # Test if it looks like a string representation of a float like '14.070'
        if len(frequency) != 9 and "." in frequency:
            frequency = float(frequency)

    # If it is a float between 0.0 and 999.999, convert it to bytes
    # This is a frequency, assumed to be expressed in MHz.
    if isinstance(frequency, float) and (0.0 < frequency < 999.99999):
        f = frequency * 1000000
        freq_str = f"{int(f):09}"

    if len(freq_str) != 9:
        logging.error(f"Error: Invalid frequency {frequency=}")
        return False

    # Create the set VFO A to frequency command
    s = "F" + vfo + freq_str + ";"
    logging.debug(s)
    # Write it to the port
    cat.write(s)

    return True


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def metervalue_type(valstr: str) -> str:
    """Get the meter value and determine the type

    :param valstr: The full string with the meter value
    :return: String with the value type

    >>> metervalue_type('RM0004000;')
    ''

    >>> metervalue_type('RM1001000;')
    'S'

    P1= 1: S 2: - 3: COMP 4: ALC 5: PO 6: SWR 7: IDD 8: VDD 9: -

    """

    valtype_dict = {
        '1': 'S',
        '2': '-',
        '3': 'COMP',
        '4': 'ALC',
        '5': 'PO',
        '6': 'SWR',
        '7': 'IDD',
        '8': 'VDD',
        '9': '-',
    }

    x = valstr[2:3]
    # print(x)
    t = valtype_dict.get(x, '')
    # print(t)
    return t


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def metervalue_to_int(valstr: str) -> int:
    """Get the meter value and convert it to an integer

    :param valstr: The full string with the meter value
    :return: Meter value as an integer

    >>> metervalue_to_int('RM0004000;')
    4

    >>> metervalue_to_int('RM1001000;')
    1

    >>> metervalue_to_int('RM1007000;')
    7

    """

    substr = valstr[3:6]
    i = int(substr)
    return i


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def read_meter() -> tuple[str, str]:
    """Read the meter value and return it

    :return: meter value
    """

    cmd = "RM" + "0"
    meter0 = cat.write(cmd)

    cmd = "RM" + "1"
    meter1 = cat.write(cmd)

    logging.debug(f"{meter0=} {meter1=}")
    return meter0, meter1


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def read_s_meter() -> int:
    """Read the S-meter value and return it as an integer

    :return: int: S-meter
    """

    cmd = "SM" + "0"
    s_meter = cat.write(cmd)

    logging.debug(f"{s_meter=}")

    substr = s_meter[3:6]
    i = int(substr)
    return i


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def scan_beacon_frequencies(port: serial.Serial, delay: float = 2.0) -> None:
    """Scan the list of beacon frequencies

    :param port: instance of serial port to use
    :param delay: Wait for delay seconds before jumping to the next frequency
    :return: Nothing
    """

    # Beacon frequeencies as strings in Hertz
    # stringlength is 9
    beacon_frequencies = [
        "014100000",
        "018110000",
        "021150000",
        "024930000",
        "028200000",
    ]

    # Get current frequency:

    cat.write("FA;")
    current_frequency = port.read_until(expected=";")
    logging.debug(f"{current_frequency=}")

    # port.write("IF;")
    # s = port.read_until(expected=";")
    # print(f"{s=}")

    for freq in beacon_frequencies:
        set_vfo(freq, "A")
        time.sleep(delay)

    cat.write(current_frequency)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# noinspection PyPep8Naming
def set_mode(mode_str: str) -> bool:
    """ Set the main band mode to the given string (i.e. 'USB', 'LSB', 'CW')

    :param mode_str: String representing the desired mode
    """

    MAIN_BAND: str = "0"
    # SUB_BAND: str = "1"

    if mode_str not in param.str_to_mode_dict.keys():
        logging.error(f"Invalide mode {mode_str=} given")
        logging.error(f"Options are {param.str_to_mode_dict.keys()}")
        return False

    mode = param.str_to_mode_dict.get(mode_str, "")
    band = MAIN_BAND
    #          P1     P2
    s = "MD" + band + mode
    cat.write(s)

    return True


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# noinspection PyPep8Naming,PyUnusedLocal
# pylint: disable=unused-variable
def reset_clarifiers() -> bool:
    """ Reset RX and TX clarifiers to OFF with an offset of 000 Hz"""

    MAIN_BAND = "0"
    SUB_BAND = "1"
    FIXED = "0"
    CLAR_SETTING = "0"
    CLAR_FREQUENCY = "1"
    RX_CLAR_OFF = "0"
    RX_CLAR_ON = "1"
    TX_CLAR_OFF = "0"
    TX_CLAR_ON = "1"

    #            P1          P2      P3             P4            P5            P6...P8
    cmd = (
        "CF"
        + MAIN_BAND
        + FIXED
        + CLAR_SETTING
        + RX_CLAR_OFF
        + TX_CLAR_OFF
        + 3 * FIXED
        + ";"
    )
    cat.write(cmd)

    #            P1          P2      P3               P4    P5...P8
    cmd = "CF" + MAIN_BAND + FIXED + CLAR_FREQUENCY + "+" + "0000" + ";"
    cat.write(cmd)

    return True


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# noinspection PyUnusedLocal,PyPep8Naming
def set_clarifier(rx_offset: [str | int]) -> bool:  # type: ignore
    """ Set TX and/or RX clarifiers.

    :param rx_offset: The offset in Hz (positive or negative).

    A value of 0Hz will turn the clarifier off.
    The offset frequency must be less than 10 kHz.

    """

    MAIN_BAND = "0"
    SUB_BAND = "1"
    FIXED = "0"
    CLAR_SETTING = "0"
    CLAR_FREQUENCY = "1"
    RX_CLAR_OFF = "0"
    RX_CLAR_ON = "1"
    TX_CLAR_OFF = "0"
    TX_CLAR_ON = "1"

    # Convert a possible integer to a 4-char string.
    # 0 will become '0000'
    rx_direction, rx_offset = offset_to_str(rx_offset)

    print(f"{rx_direction=} {rx_offset=}")

    # If the offset is 0 or '0000', then turn of the RX clarifier
    rx_clar_onoff = RX_CLAR_OFF
    if int(rx_offset):
        rx_clar_onoff = RX_CLAR_ON

    # Set the RX Clarifier frequency
    #            P1          P2      P3               P4    P5...P8
    cmd = 'CF' + MAIN_BAND + FIXED + CLAR_FREQUENCY + rx_direction + rx_offset + ";"
    cat.write(cmd)

    # Turn the RX Clarifier on or off
    #            P1          P2      P3             P4        P5        P6...P8
    cmd = 'CF' + MAIN_BAND + FIXED + CLAR_SETTING + rx_clar_onoff + TX_CLAR_OFF + 3 * FIXED + ";"
    cat.write(cmd)

    return True


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def main() -> None:
    """ main entry point."""

    # cat.show_serial_ports()

    port = cat.open_cat_port()
    param.port = port  # Save the CAT port

    # get_information()
    # reset_clarifiers()
    # set_clarifier(rx_offset=0)

    while True:
        # m0, m1 = read_meter()
        # print(m0, m1)
        # i = metervalue_to_int(m0)
        # j = metervalue_type(m1)
        # k = metervalue_to_int(m1)
        # print(i, j, k)

        s = read_s_meter()
        print(f"{s=}", end=", ", flush=True)
        time.sleep(0.25)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
