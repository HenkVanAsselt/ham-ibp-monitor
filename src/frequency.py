"""Commandline interface to set the TRX to a specific frequency."""

# Global imports
import logging
from typing import Union
import re

# 3rd party imports
import click

# local imports
import cat
import param
import transceiver


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def freq_or_meter_to_freq(p: int | float | str) -> int:
    """Convert frequency or band to the bottom frequency.

    :param p: The input to handle

    :returns: Lowest frequency as an integer. Returns 0 in case of an error

    >>> freq_or_meter_to_freq(20)       # 20 meter band
    14

    >>> freq_or_meter_to_freq(18.100)   # 18 MHz as a float
    18

    >>> freq_or_meter_to_freq("21.100") # 21 MHz as a string
    21

    >>> freq_or_meter_to_freq("10")     # 10 meter band as a string
    28

    >>> freq_or_meter_to_freq("80")     # Invalid 80 meter band
    0

    >>> freq_or_meter_to_freq("")       # Empty string
    0

    >>> freq_or_meter_to_freq("20m")       # With a band indictor
    14

    >>> freq_or_meter_to_freq("14.100 MHz")   # With a frequency indicator
    14

    """

    # Dictionary to convert meters (as integer) to frequency (in MHz)
    m_to_f: dict[int, int] = {
        20: 14,  # 20 meter = 14 MHz
        17: 18,  # 17 meter = 18 MHz
        15: 21,  # 15 meter = 21 MHz
        12: 24,  # 12 meter = 24 MHz
        10: 28,  # 10 meter = 28 MHz
    }

    if isinstance(p, int):
        x = p
    elif isinstance(p, float):
        x = int(p)
    elif isinstance(p, str):
        if not p:
            logging.error("Cannot convert an empty string")
            return 0
        r: str = re.search("[0-9.,]+", p).group()
        x = int(float(r))
    else:
        logging.error(f"Unknown type {type(p)} for parameter {p}")
        return 0

    if x in m_to_f.values():
        return x
    if x in m_to_f:
        return m_to_f[x]

    logging.error(f"Unsupported frequency or band {p}")
    return 0


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
@click.command()
@click.option("--vfo", default="A", help="VFO to use (A or B), A is the default")
@click.option("--freq", "-f", prompt="Frequency", help="Frequency to set (i.e 14.070")
def set_frequency(vfo: str, freq: Union[str, float]) -> None:
    """Set the TRX to the given frequency on the given VFO"""

    port = cat.open_cat_port()
    param.port = port  # Save the CAT port

    transceiver.set_vfo(freq, vfo=vfo)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    set_frequency()
