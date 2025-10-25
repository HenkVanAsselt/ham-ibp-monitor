"""Based on current time, calculate which beacon cycle we are in."""

# pylint: disable=unnecessary-ellipsis,logging-fstring-interpolation,

import logging
import math

# global imports
import time
from typing import Any

# 3rd party imports
from rich.console import Console

# local imports
import beacons
import frequency
import param

console = Console()


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def current_cycle() -> tuple[int, int]:
    """Calculate the current cycle and seconds in that cycle.

    :returns: tuple of cycle number and seconds in that cycle

    Note: A cycle lasts 180 seconds
    """

    curtime = time.gmtime()
    seconds_since_midnight = (
        curtime.tm_hour * 3600 + curtime.tm_min * 60 + curtime.tm_sec
    )
    cycle = math.floor(seconds_since_midnight / 180)
    seconds_in_cycle = seconds_since_midnight - (180 * cycle)

    return cycle, seconds_in_cycle


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def print_beacon_on_freq(freq: [int | str]) -> None:  # type: ignore
    """Determine the current transmitting beacon on the given frequency

    :param freq: Frequency band in MHz like 14, 18, 21, 24, 28
    """

    cycle, seconds = current_cycle()
    slot = math.floor(seconds / 10)
    logging.debug(f"{cycle=} {seconds=} {slot=}\n")

    if not beacons.dict_of_beacons:
        beacons.dict_of_beacons = beacons.get_dict_of_beacons()

    # Show current list of transmitting beacons.

    if int(freq) == 14:
        n = slot
    elif int(freq) == 18:
        n = slot - 1
    elif int(freq) == 21:
        n = slot - 2
    elif int(freq) == 24:
        n = slot - 3
    elif int(freq) == 28:
        n = slot - 4
    else:
        print(f"Invalid frequency {freq}")
        return

    # Compensate for the wrap-around through the list.
    # It is an ugly solution, but it works.
    if n < 0:
        n += 18

    print(f"{freq} MHz: {beacons.dict_of_beacons[n]}")


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def get_current_slot_on_frequency(freq: Any) -> int:
    """Determine the current transmitting beacon on the given frequency

    :param freq: Frequency band in MHz like 14, 18, 21, 24, 28
    :returns: Current slot, 0 in case of an error
    """

    freq = frequency.freq_or_meter_to_freq(freq)

    cycle, seconds = current_cycle()
    slot = math.floor(seconds / 10)
    logging.debug(f"{cycle=} {seconds=} {slot=}\n")

    # Determine current beacon on the given frequency

    if int(freq) == 14:  # 20 meter band
        n = slot
    elif int(freq) == 18:  # 17 meter band
        n = slot - 1
    elif int(freq) == 21:  # 15 meter band
        n = slot - 2
    elif int(freq) == 24:  # 12 meter band
        n = slot - 3
    elif int(freq) == 28:  # 10 meter band
        n = slot - 4
    else:
        print(f"Invalid frequency {freq}")
        return 0

    # Compensate for the wrap-around through the list.
    # It is an ugly solution, but it works.
    if n < 0:
        n += 18

    # return f"{freq} MHz: {bcns[n]}"
    return n


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def show_transmitting_beacons() -> None:
    """Show a list of currently transmitting beacons."""

    cycle, seconds = current_cycle()
    slot = math.floor(seconds / 10)
    print(f"{cycle=} {seconds=} {slot=}\n")

    bcns = beacons.get_dict_of_beacons()

    # Show current list of transmitting beacons.
    # Compensate for the wrap-around through the list.
    # It is an ugly solution, but it works.

    n = slot
    if n < 0:
        n += 18
    console.print(f"14.100 MHz: {bcns[n]}")

    n = slot - 1
    if n < 0:
        n += 18
    console.print(f"18.110 MHz: {bcns[n]}")

    n = slot - 2
    if n < 0:
        n += 18
    console.print(f"21.150 MHz: {bcns[n]}")

    n = slot - 3
    if n < 0:
        n += 18
    console.print(f"24.930 MHz: {bcns[n]}")

    n = slot - 4
    if n < 0:
        n += 18
    console.print(f"28.200 MHz: {bcns[n]}")


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def main() -> None:
    """main entry point"""
    ...


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
