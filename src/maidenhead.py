""" Maidenhead calculations (distance and bearing)
"""

""" Calculate distance between 2 maidenhead locations."""

# Leigh L. Klotz, Jr.
# WA5ZNU
# Origin: https://wa5znu.org/2007/08/bearing/

import logging
import sys
from math import sin, cos, atan2, pi, sqrt

RADIUS = 6367000.0

# Beam rotor offset correction here (or use command-line arg)
offset = 0


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def latlon(qra: str) -> tuple[float, float]:
    """Convert the given maidenhead locator to lat and long

    :param qra: The maidenhead locator
    :return: tuple of latitude and longitude
    """

    c1 = int(qra[0:1], 36) - 10
    c2 = int(qra[1:2], 36) - 10
    c3 = int(qra[2:3], 10)
    c4 = int(qra[3:4], 10)
    if len(qra) > 4:
        c5 = int(qra[4:5], 36) - 10
        c6 = int(qra[5:6], 36) - 10
        lat = ((c2 * 10) + c4 + ((c6 + 0.5) / 24)) - 90
        lon = ((c1 * 20) + (c3 * 2) + ((c5 + 0.5) / 12)) - 180
    else:
        lat = ((c2 * 10) + c4) - 90
        lon = ((c1 * 20) + (c3 * 2)) - 180
    return lat, lon


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def latlon_distance(lat1r: float, lon1r: float, lat2r: float, lon2r: float) -> int:
    """ Calculate the distance between 2 lat/lon locations.

    :param lat1r: position 1 lattitude
    :param lon1r: position 1 longitude
    :param lat2r: position 2 lattitude
    :param lon2r: position 2 longitude

    :return: Distance in kilometers

    Uses haversine greatcircle calculation
    """

    dlonr = lon2r - lon1r
    dlatr = lat2r - lat1r
    a = ((sin(dlatr / 2.0)) * (sin(dlatr / 2.0))) + (
        cos(lat1r) * cos(lat2r) * (sin(dlonr / 2.0)) * (sin(dlonr / 2.0))
    )
    c = 2 * (atan2(sqrt(a), (sqrt(1.0 - a))))
    d = RADIUS * c
    return int(d / 1000.0)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def maidenhead_distance(loc1: str, loc2: str) -> int:
    """Calculate the distance between the maidenhead locations

    :param loc1: Location 1
    :param loc2: Location 2

    :return: Distance in kilometers

    Uses haversine greatcircle calculation

    >>> maidenhead_distance('JO22lm', 'FJ69cc')      # Caracas, Venuzuela
    8036

    >>> maidenhead_distance('JO22lm', 'OL72bg')      # Hong Kong
    9261

    >>> maidenhead_distance('JO22lm', 'JO22lm')      # Same location
    0
    """

    (lat1, lon1) = latlon(loc1)
    logging.debug(f"{loc1=}, {lat1=}, {lon1=}")

    (lat2, lon2) = latlon(loc2)
    logging.debug(f"{loc2=}, {lat2=}, {lon2=}")

    k = 180.0 / pi

    lat1r = lat1 / k
    lon1r = lon1 / k

    lat2r = lat2 / k
    lon2r = lon2 / k

    dist_km = latlon_distance(lat1r, lon1r, lat2r, lon2r)
    return int(dist_km)


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def latlon_bearing(lat1r: float, lon1r: float, lat2r: float, lon2r: float) -> int:
    """ Calculate the bearing between 2 lat/lon locations

    :param lat1r: position 1 lattitude
    :param lon1r: position 1 longitude
    :param lat2r: position 2 lattitude
    :param lon2r: position 2 longitude

    :return: The bearing in degrees.
    """

    k = 180.0 / pi

    dlong = lon2r - lon1r
    # dlat = lat2r - lat1r

    arg1 = sin(dlong) * cos(lat2r)
    arg2a = cos(lat1r) * sin(lat2r)
    arg2b = sin(lat1r) * cos(lat2r) * cos(dlong)
    arg2 = arg2a - arg2b
    bearingr = atan2(arg1, arg2)

    bearing = round(((360 + (bearingr * k)) % 360))
    bearing = bearing + offset

    # print("%d/%d" % (bearing, antibearing))

    return bearing


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def maidenhead_bearing(loc1: str, loc2: str) -> int:
    """ Calculate bearing from maidenhead location to maidenhead location.

    :param loc1: Location 1
    :param loc2: Location 2

    :return: Bearing in degrees

    >>> maidenhead_bearing('JO22lm', 'FJ69cc')      # Caracas, Venuzuela
    262

    >>> maidenhead_bearing('JO22lm', 'OL72bg')      # Hong Kong
    62

    >>> maidenhead_bearing('JO22lm', 'JO22lm')      # own location
    0

    """

    (lat1, lon1) = latlon(loc1)
    logging.debug(f"{loc1=}, {lat1=}, {lon1=}")

    (lat2, lon2) = latlon(loc2)
    logging.debug(f"{loc2=}, {lat2=}, {lon2=}")

    k = 180.0 / pi

    lat1r = lat1 / k
    lon1r = lon1 / k

    lat2r = lat2 / k
    lon2r = lon2 / k

    bearing = latlon_bearing(lat1r, lon1r, lat2r, lon2r)
    logging.debug(f"{bearing=}")
    return bearing


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def main() -> None:
    """main function."""

    # Set your QRA here
    own_locator = "JO22lm"
    (lat1, lon1) = latlon(own_locator)
    logging.debug(f"{own_locator=}, {lat1=}, {lon1=}")

    other_locator = sys.argv[1]
    (lat2, lon2) = latlon(other_locator)
    logging.debug(f"{other_locator=}, {lat2=}, {lon2=}")

    # k = 180.0 / pi
    #
    # lat1r = lat1 / k
    # lon1r = lon1 / k
    #
    # lat2r = lat2 / k
    # lon2r = lon2 / k

    # distkm = latlon_distance(lat1r, lon1r, lat2r, lon2r)
    # # distmi = 0.621371192 * distkm   # Convert kilometers to miles
    # b = latlon_bearing(lat1r, lon1r, lat2r, lon2r)
    # print("Distance: %g km, bearing=%g degrees" % (distkm, b))

    distkm = maidenhead_distance(own_locator, other_locator)
    b = maidenhead_bearing(own_locator, other_locator)
    print("Distance: %g km, Bearing: %g degrees" % (distkm, b))


# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)

    if len(sys.argv) == 1:
        print("usage: maidenhead_distance dxqra")
        sys.exit(1)

    if not len(sys.argv) == 2:
        print("2 arguments required")
        sys.exit(1)

    main()
