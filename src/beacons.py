""" Read and process the file config/Beacons.lst
"""

# pylint: disable=logging-fstring-interpolation, line-too-long

# Global imports
from configparser import ConfigParser
from dataclasses import dataclass
import logging

# Local imports
from src import param


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
@dataclass
class Beacon:
    """ Dataclass to store beacon information in.
    """
    slot: int
    callsign: str
    dx_entity: str
    city: str
    grid_locator: str


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def get_dict_of_beacons(configfile: str = "./config/config.ini") -> dict[int, Beacon]:
    """Read the configfile with beacon information

    :return: dictionary of beacons (number and name)

    Contents of the latest config.ini (extracted from https://www.ncdxf.org/beacon/beaconlocations.html)::

        [BEACONS]
        # Slot = Callsign, City, Country, Grid Square
        0 =  4U1UN, New York City, United Nations, FN30as
        1 =  VE8AT, Inuvik NT, Canada, CP38gh
        2 =  W6WX, Mt. Umunhum, United States, CM97bd
        3 =  KH6RS, Maui, Hawaii, BL10ts
        4 =  ZL6B, Masterton, New Zealand, RE78tw
        5 =  VK6RBP, Rolystone, Australia, OF87av
        6 =  JA2IGY, Mt. Asama, Japan, PM84jk
        7 =  RR9O, Novosibirsk, Russia, NO14kx
        8 =  VR2B, Hong Kong, Hong Kong, OL72bg
        9 =  4S7B, Colombo, Sri Lanka, MJ96wv
        10 = ZS6DN, Pretoria, South Africa, KG33xi
        11 = 5Z4B, Kariobangi, Kenya, KI88ks
        12 = 4X6TU, Tel Aviv, Israel, KM72jb
        13 = OH2B, Lohja, Finland, KP20eh
        14 = CS3B, São Jorge, Madeira, IM12mt
        15 = LU4AA, Buenos Aires, Argentina, GF05tj
        16 = OA4B, Lima, Peru, FH17mw
        17 = YV5B, Caracas, Venezuela, FJ69cc


    """

    beacons_ini = ConfigParser()
    beacons_ini.read(configfile)

    # Turn the information into a dictionary of Beacon dataclasses
    beacon_dict: dict[int, Beacon] = {}
    for slotstr, value in beacons_ini.items("BEACONS"):
        slot = int(slotstr)
        callsign, city, country, grid_locator = value.split(",")
        b = Beacon(
            slot,
            callsign.strip(),
            country.strip(),
            city.strip(),
            grid_locator.strip(),
        )
        beacon_dict[slot] = b

    logging.debug(f"{beacon_dict=}")
    param.beacons = beacon_dict
    return beacon_dict


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def show_beacons(beacons: dict[int, Beacon]) -> None:
    """ Print the list of beacons.

    :param beacons: dictionary of beacons
    """

    # slot: int
    # callsign: str
    # dx_entity: str
    # city: str
    # grid_locator: str

    for b in beacons.values():
        print(f"{b.slot}: {b.callsign}, {b.city}, {b.dx_entity}, {b.grid_locator}")


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
def main() -> None:
    """ main function

    :return: Nothing
    """

    beacons = get_dict_of_beacons("./config/config.ini")
    show_beacons(beacons)


# ----------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
