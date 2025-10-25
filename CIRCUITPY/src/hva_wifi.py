import sys
import os
import time
import wifi
import rtc
import adafruit_connection_manager  # type: ignore
import adafruit_ntp                 # type: ignore

def scan():
    print("Available WiFi networks")
    print("-----------------------")
    networks = []
    for network in wifi.radio.start_scanning_networks():
        networks.append(network)
    wifi.radio.stop_scanning_networks()
    networks = sorted(networks, key=lambda net: net.rssi, reverse=True)
    for network in networks:
       print(f"{network.ssid} {network.rssi}")

def connect():
    """The SSID and PSK are stored in 'settings.toml'"""
    print("Connecting to WiFi")
    ssid = os.getenv("CIRCUITPY_WIFI_SSID")
    psk = os.getenv("CIRCUITPY_WIFI_PASSWORD")
    wifi.radio.connect(ssid, psk)
    print(f"Connected to {ssid}")


def synctime():
    try:
        t = time.localtime()
        print("time before sync", t)
        pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
        ntp = adafruit_ntp.NTP(pool, tz_offset=0, cache_seconds=3600)
        print(f"{ntp.utc_ns=}")
        print(f"{ntp.datetime=}")
        # NOTE: This changes the system time so make sure you aren't assuming that time
        # doesn't jump.
        rtc.RTC().datetime = ntp.datetime
        t = time.localtime()
        print("time after sync", t)
    except OSError:
        pass
