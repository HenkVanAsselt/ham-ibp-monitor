"""Determine available serial ports and determine which one if for the CAT interface."""

# pylint: disable=invalid-name, logging-fstring-interpolation

import sys
import logging

# 3rd party imports
import serial  # type: ignore
from serial.tools.list_ports import comports  # type: ignore

# local imports
import param

logging.basicConfig(level=logging.INFO)


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def show_serial_ports() -> None:
    """Show the avaialble serial ports

    :return: Nothing
    """

    sys.stderr.write("\n--- Available ports:\n")

    # Show the ports
    for n, (port, desc, _hwid) in enumerate(sorted(comports()), 1):
        sys.stderr.write(
            "--- {:2}: {:20} {!r}\n".format(n, port, desc)
        )  # pylint:disable=consider-using-f-string


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def get_cat_port() -> str:
    """Get the serial port which acts as the CAT port

    :return: port as string, for example 'COM6:'
    """

    for _n, (port, desc, _hwid) in enumerate(sorted(comports()), 1):
        if "Silicon Labs Dual CP2105 USB to UART Bridge: Enhanced COM Port" in desc:
            return str(port)

    # Default: return nothing
    return ""


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def open_cat_port(cat_port: str = "") -> serial.Serial:
    """Open the serial CAT port

    :param cat_port: If given, use this port (for example 'COM6:')
                     If no port is given, determine it now.

    :return: instance of the opened serial port.
    """

    logging.debug("Trying to open CAT port")

    if not cat_port:
        cat_port = get_cat_port()
        if not cat_port:
            print("Error: Could not find a CAT port to open")
            sys.exit(-1)

    logging.debug(f"{cat_port=}")
    port = serial.Serial(cat_port, baudrate=38400, timeout=0.1)
    logging.debug(f"{port=}")
    return port


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def write(cmd: str | bytes) -> str:
    """Write the given command to the CAT port

    :param cmd: The command (string or bytearray) to send
    :returns: Response (if any)

    If a string is given, then it will be converted to a bytearray.
    If the terminator ';' was not present, it will be added here.
    If no CAT port was opened, it will be opened here

    """

    b = cmd
    if isinstance(cmd, str):
        # Add the termination character if neccessary
        if not cmd.endswith(";"):
            cmd += ";"
        b = cmd.encode("utf-8")
    elif isinstance(cmd, bytes):
        # Add the termination character if neccessary
        if not cmd.endswith(b";"):
            cmd += b";"
    else:
        logging.error("Invalid cmd format. Must be str or bytes")

    if not param.port:
        param.port = open_cat_port()

    param.port.write(b)

    # Check if there is a response. If so, log it
    response = param.port.read_until(expected=";")
    if response:
        logging.debug(f"{response=}")
        ret: str = response.decode("utf-8")
        return ret

    return ""  # Default is an empty string


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def main() -> None:
    """Show all serial ports, then determine and show the CAT port

    :return: Nothing
    """

    show_serial_ports()
    s = get_cat_port()
    print()
    print(f"CAT port = {s}")


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
