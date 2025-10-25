import sys
import time
import math

import hva_wifi
hva_wifi.connect()
hva_wifi.synctime()

# At this point, we do not need WiFi anymore
import gc
gc.enable()
del hva_wifi
gc.collect()

# Intialize the Pimoroni display
import pimoroni_pico_display
display, line1, line2, line3, line4, line5, line6 = pimoroni_pico_display.display_layout()

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def show_current_time(time_tuple, line1):

    line1.text = f"{time_tuple[0]}{time_tuple[1]:02d}{time_tuple[2]:02d} {time_tuple[3]:02d}:{time_tuple[4]:02d}:{time_tuple[5]:02d}"

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------
def current_cycle(time_tuple) -> tuple[int, int]:
    """Calculate the current cycle and seconds in that cycle.

    :returns: tuple of cycle number and seconds in that cycle

    Note: A cycle lasts 3 mintues (180 seconds)
    """

    # curtime = time.gmtime()
    seconds_since_midnight = (
        # hours * 3600 + minutes * 60 + seconds
        # curtime.tm_hour * 3600 + curtime.tm_min * 60 + curtime.tm_sec
        time_tuple.tm_hour * 3600 + time_tuple.tm_min * 60 + time_tuple.tm_sec
    )
    cycle = math.floor(seconds_since_midnight / 180)
    seconds_in_cycle = seconds_since_midnight - (180 * cycle)

    return cycle, seconds_in_cycle


"""
beacons = {
0 :  "4U1UN, New York City, United Nations, FN30as",
1 :  "VE8AT, Inuvik NT, Canada, CP38gh",
2 :  "W6WX, Mt. Umunhum, United States, CM97bd",
3 :  "KH6RS, Maui, Hawaii, BL10ts",
4 :  "ZL6B, Masterton, New Zealand, RE78tw",
5 :  "VK6RBP, Rolystone, Australia, OF87av",
6 :  "JA2IGY, Mt. Asama, Japan, PM84jk",
7 :  "RR9O, Novosibirsk, Russia, NO14kx",
8 :  "VR2B, Hong Kong, Hong Kong, OL72bg",
9 :  "4S7B, Colombo, Sri Lanka, MJ96wv",
10 : "ZS6DN, Pretoria, South Africa, KG33xi",
11 : "5Z4B, Kariobangi, Kenya, KI88ks",
12 : "4X6TU, Tel Aviv, Israel, KM72jb",
13 : "OH2B, Lohja, Finland, KP20eh",
14 : "CS3B, São Jorge, Madeira, IM12mt",
15 : "LU4AA, Buenos Aires, Argentina, GF05tj",
16 : "OA4B, Lima, Peru, FH17mw",
17 : "YV5B, Caracas, Venezuela, FJ69cc",
}
"""

# Simplified beacon list to fit the pimoroni_pico_display
beacons = {
0 :  "4U1UN,New York",
1 :  "VE8AT,Canada",
2 :  "W6WX,United States",
3 :  "KH6RS,Hawaii",
4 :  "ZL6B,New Zealand",
5 :  "VK6RBP,Australia",
6 :  "JA2IGY,Japan",
7 :  "RR9O,Russia",
8 :  "VR2B,Hong Kong",
9 :  "4S7B,Sri Lanka",
10 : "ZS6DN,South Africa",
11 : "5Z4B,Kenya",
12 : "4X6TU,Israel",
13 : "OH2B,Finland",
14 : "CS3B,Madeira",
15 : "LU4AA,Argentina",
16 : "OA4B,Peru",
17 : "YV5B,Venezuela",
}

for nr, info in beacons.items():
    print(nr, info)




while True:
    time_tuple = time.localtime()  # time in seconds since Epoch as 8-tuple
    # print(f"{time_tuple=}")
    show_current_time(time_tuple, line1)
    cycle, secs_in_cycle = current_cycle(time_tuple)
    slot = math.floor(secs_in_cycle / 10)
    # print(f"{cycle=} {secs_in_cycle=} {slot=}")

    # Show transmitting beacons
    # Compensate for the wrap-around through the list.
    # It is an ugly solution, but it works.
    n = slot
    if n < 0:
        n += 18
    line2.text = f"14.100:{beacons[n]}"

    n = slot - 1
    if n < 0:
        n += 18
    line3.text = f"18.110:{beacons[n]}"

    n = slot - 2
    if n < 0:
        n += 18
    line4.text = f"21.150:{beacons[n]}"

    n = slot - 3
    if n < 0:
        n += 18
    line5.text = f"24.930:{beacons[n]}"

    n = slot - 4
    if n < 0:
        n += 18
    line6.text = f"28.200:{beacons[n]}"

    time.sleep(0.25)
