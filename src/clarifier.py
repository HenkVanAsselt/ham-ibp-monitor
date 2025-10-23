""" Commandline interface to set the RX and TX clarifiers. """


# Global imports
# import sys

# 3rd party imports
import click

# local imports
from src import cat
from src import param
from src import transceiver


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
@click.command()
@click.option("--rx", help="RX Clarifier offset", default='0000')
@click.option("--reset", is_flag=True, help="Reset TX and RX clarifiers to default settings")
def set_clarifier(rx, reset) -> None:  # type: ignore
    """Set the TRX to the given frequency on the given VFO"""

    print(f"{rx=}")

    if not rx:
        print("No clarifier offset given")
        return

    port = cat.open_cat_port()
    param.port = port  # Save the CAT port

    if reset:
        transceiver.reset_clarifiers()
        return

    return


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    set_clarifier()
