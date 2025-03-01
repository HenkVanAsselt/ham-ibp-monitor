Ham IPB (International Beacon Project) Monitor
##############################################

**Ham IPB (International Beacon Project) Monitor, written in Python.**

This project was started as there are such monitors, but no source code available, and Faros could not program my
Yeasu FTdx10 properly (it went to transmit mode immediately)

IBP Background
==============

- The beacons are transmitted on the frequencies 14.100 MHz, 18.110 MHz, 21.150 MHz, 24.930 MHz and 28.200 MHz.
- Each beacon transmission site operates around the clock.
- Beacon is transmitted once on each frequency, from low (14.100 MHz) to high (28.200 MHz), followed by a 130-second pause after which the cycle is repeated.
- Each transmission is 10 second long, and consists of the call sign of the beacon transmitted at 22 words per minute (WPM) followed by four dashes.
- The call sign and the first dash is transmitted at 100 watts of power. Subsequent three dashes are transmitted at 10 watts, 1 watt and 0.1 watt respectively.
- All beacon transmissions are coordinated using GPS time. As such, at a given frequency, all 18 beacons are transmitted once every three minutes.

List of beacons::

    Slot    Beacon          Call    Location        Grid    Operator
    1       United Nations  4U1UN   New York City   FN30as  United Nations Staff Recreation Council Amateur Radio Club (UNRC)
    2       Canada          VE8AT   Eureka, Nunavut EQ79ax  Radio Amateurs Canada (RAC) / Northern Alberta Radio Club (NARC)
    3       United States   W6WX    Mt. Umunhum     CM97bd  Northern California DX Foundation (NCDXF)
    4       Hawaii          KH6RS   Maui            BL10ts  Maui Amateur Radio Club (Maui ARC)
    5       New Zealand     ZL6B    Masterton       RE78tw  New Zealand Association of Radio Transmitters (NZART)
    6       Australia       VK6RBP  Roleystone      OF87av  Wireless Institute of Australia (WIA)
    7       Japan J         A2IGY   Mt. Asama       PM84jk  Japan Amateur Radio League (JARL)
    8       Russia          RR9O    Novosibirsk     NO14kx  Russian Amateur Radio Union (SRR)
    9       Hong Kong       VR2B    Hong Kong       OL72bg  Hong Kong Amateur Radio Transmitting Society (HARTS)
    10      Sri Lanka       4S7B    Colombo         MJ96wv  Radio Society of Sri Lanka (RSSL)
    11      South Africa    ZS6DN   Pretoria        KG44dc  ZS6DN
    12      Kenya           5Z4B    Kariobangi      KI88ks  Amateur Radio Society of Kenya (ARSK)
    13      Israel          4X6TU   Tel Aviv        KM72jb  Israel Amateur Radio Club (IARC)
    14      Finland         OH2B    Lohja           KP20eh  Finnish Amateur Radio League (SRAL)
    15      Madeira         CS3B    Santo da Serra  IM12or  Rede dos Emissores Portugueses (REP)
    16      Argentina       LU4AA   Buenos Aires    GF05tj  Radio Club Argentino (RCA)
    17      Peru            OA4B    Lima            FH17mw  Radio Club Peruano (RCP)
    18      Venezuela       YV5B    Caracas         FJ69cc  Radio Club Venezolano (RCV)

For an webbased view of wich beacon is transmitting, see https://www.ncdxf.org/beacon/index.html#transmission

ham-ipb-monitor Features
------------------------

- Shows which beacon is currently transmitting on which frequency.
- By means of a CAT interface, will tune the receiver to one of the beacon frequencies.
- First text only output will be written, followed by a GUI using PySide6.
- Strategies:
  - Follow a specific beacon over all possible frequencies, or
  - Stay on one frequency to monitor all possible beacons

Requirements
------------

- Virtual COM port driver from http://www.yaesu.com

After the installation and connection to the tranceiver, you should see 2 ports in the Windows device manager.

- `Silicon Labs Dual CP210x USB to UART Bridge: Enhanced COM Port (COMxx)`

    The **Enhanced COM Port** is for CAT Communications (Frequency and Comminication Mode Settings)

- `Silicon Labs Dual CP210x USB to UART Bridge: Standard COM Port (COMxx)`

    The **Standard COM Port** is for TX Controls (PTT Control, CW Keying, Digital Mode Operation)



