""" Commandline interface to set the TRX to a specific mode. """


# Global imports

# 3rd party imports
import click

# local imports
import param
import cat
import transceiver


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
@click.command()
@click.option("--mode", prompt="Mode", help="Set mode")

def set_mode(mode: str) -> None:
    """Set the TRX to the given mode."""

    port = cat.open_cat_port()
    param.port = port  # Save the CAT port

    if mode not in param.mode_dict.values():
        print(f"Error: Unknown mode {mode}")
        valid_modes = ', '.join(param.mode_dict.values())
        print(f"Valid modes are {valid_modes}")
        return

    transceiver.set_mode(mode)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
# pylint: disable=no-value-for-parameter
if __name__ == "__main__":
    set_mode()
