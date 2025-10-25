import board
import busio
import terminalio
import displayio
import time

# Starting in CircuitPython 9.x fourwire will be a seperate internal library
# rather than a component of the displayio library
try:
    from fourwire import FourWire
except ImportError:
    from displayio import FourWire
from adafruit_display_text import label
from adafruit_st7789 import ST7789  # type: ignore

# First set some parameters used for shapes and text
BORDER = 2
FONTSCALE = 2
BACKGROUND_COLOR = 0x66B2FF  # Blue
FOREGROUND_COLOR = 0x606060  # Grey
TEXT_COLOR = 0xFFFF00 # Yellow

def init_display():

    # Release any resources currently in use for the displays
    displayio.release_displays()

    tft_cs = board.GP17
    tft_dc = board.GP16
    spi_mosi = board.GP19
    spi_clk = board.GP18
    spi = busio.SPI(spi_clk, spi_mosi)

    display_bus = FourWire(spi, command=tft_dc, chip_select=tft_cs)
    display = ST7789(
        display_bus, rotation=270, width=240, height=135, rowstart=40, colstart=53  # always use these numbers
    )

    # Make the display context
    splash = displayio.Group()
    display.root_group = splash
    return display, splash

def display_layout():
    display, _splash = init_display()
    # display.root_group = _splash

    color_bitmap = displayio.Bitmap(display.width, display.height, 1)
    color_palette = displayio.Palette(1)
    color_palette[0] = BACKGROUND_COLOR
    bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
    # _splash.append(bg_sprite)
    display.root_group.append(bg_sprite)

    # Draw a smaller inner rectangle
    inner_bitmap = displayio.Bitmap(
        display.width - BORDER * 2, display.height - BORDER * 2, 1
    )
    inner_palette = displayio.Palette(1)
    inner_palette[0] = FOREGROUND_COLOR
    inner_sprite = displayio.TileGrid(
        inner_bitmap, pixel_shader=inner_palette, x=BORDER, y=BORDER
    )
    display.root_group.append(inner_sprite)

    font = terminalio.FONT

    # Draw label 1
    text = ""
    label1 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width1 = label1.bounding_box[2] * FONTSCALE
    text_group1 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 10,
    )
    text_group1.append(label1)
    display.root_group.append(text_group1)

    # Draw label 2
    text = ""
    label2 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width2 = label2.bounding_box[2] * FONTSCALE
    text_group2 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 40,
    )
    text_group2.append(label2)
    display.root_group.append(text_group2)

    # Draw label 3
    text = ""
    label3 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width3 = label3.bounding_box[2] * FONTSCALE
    text_group3 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 60,
    )
    text_group3.append(label3)
    display.root_group.append(text_group3)

    # Draw label 4
    text = ""
    label4 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width4 = label4.bounding_box[2] * FONTSCALE
    text_group4 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 80,
    )
    text_group4.append(label4)
    display.root_group.append(text_group4)

    # Draw label 5
    text = ""
    label5 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width5 = label5.bounding_box[2] * FONTSCALE
    text_group5 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 100,
    )
    text_group5.append(label5)
    display.root_group.append(text_group5)

    # Draw label 6
    text = ""
    label6 = label.Label(font, text=text, color=TEXT_COLOR)
    text_width6 = label6.bounding_box[2] * FONTSCALE
    text_group6 = displayio.Group(
        scale=FONTSCALE,
        x=BORDER + 5,
        y=BORDER + 120,
    )
    text_group6.append(label6)
    display.root_group.append(text_group6)

    return display, label1, label2, label3, label4, label5, label6

if __name__ == '__main__':
    display, label1, label2, label3, label4, label5, label6 = display_layout()


