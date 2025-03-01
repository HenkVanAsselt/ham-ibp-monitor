"""Commandline interface to show the current beacon for a given band"""

# pylint: disable=logging-fstring-interpolation

# Global imports
import sys
import signal
import time
import logging

# 3rd party imports
import click

# 3rd party imports
from rich.console import Console

# Local import
from src import param
from src import beacons
from src import cycle_calculator
from src import frequency
from src import transceiver

console = Console()


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def signal_handler(signal_obj: object, frame: object) -> None:
    """Called after CTRL+C is detected.

    :param signal_obj:
    :param frame:
    :return:
    """

    print()
    print("\nCtrl+C detected. Closing program")
    print(f"{signal_obj=}, {frame=}")
    sys.exit(0)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
@click.command()
@click.option(
    "--band",
    is_flag=False,
    flag_value=20,
    default=20,
    help="Show beacons on the given HAM band",
)
@click.option(
    "--tune", is_flag=True, default=False, help="Tune trx to the given frequency band"
)
def show(band, tune) -> None:
    """Show beacons on the given HAM band"""

    console.print("\nHAM International Beacon Project monitor\n")

    f = frequency.freq_or_meter_to_freq(band)
    if not f:
        print(f"Invalid argument {band}")
        sys.exit(1)

    print(f"Current beacon on {f} MHz:")

    if tune:
        mode = "CW-U"
        logging.info(f"Setting the radio to {f} {mode}")
        # Get the real frequency instead of just the indicator 14, 21, 28 etc.
        freq = param.beacon_frequency.get(f)
        transceiver.set_vfo(frequency=freq)
        transceiver.set_mode(mode)

    signal.signal(signal.SIGINT, signal_handler)
    old_slot: int = 0
    color: str = "[bold red]"
    with console.status("Initial status", spinner="bouncingBall") as status:
        while True:
            current_slot = cycle_calculator.get_current_slot_on_frequency(f)
            if current_slot != old_slot:
                # print("New slot")
                old_slot = current_slot
                if current_slot % 2 == 0:
                    color = "[bold red]"
                else:
                    color = "[bold blue]"
            beacon = param.beacons[current_slot]
            status.update(f"{color} {beacon}")
            time.sleep(0.25)  # or do some more work


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# pylint: disable=no-value-for-parameter
if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG)
    beacons.get_dict_of_beacons()
    show()
