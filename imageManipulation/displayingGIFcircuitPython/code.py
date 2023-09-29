import os, sys
import board
import busio
import terminalio
import displayio

from adafruit_st7735r import ST7735R
import adafruit_st7789
import time
import gifio

# Release any resources currently in use for the displays
displayio.release_displays()

#===init display ======================
disp_blk = board.RGB
disp_cs  = board.GP18
disp_dc  = board.GP16
disp_res = board.GP17

mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = ST7735R(display_bus, width=128, height=160, bgr = True)
'''
disp_mosi = board.GP11
disp_clk = board.GP10
disp_spi = busio.SPI(clock=disp_clk,
                     MOSI=disp_mosi)

display_bus = displayio.FourWire(
    disp_spi,
    command=disp_dc,
    chip_select=disp_cs,
    reset=disp_res
)

#--- Setup display ---

# for 1.14" 135x240 (RGB) IPS
display = adafruit_st7789.ST7789(display_bus,
                                 width=130,
                                 height=161,
                                 rowstart=0, colstart=0,
                                 rotation=0,
                                 backlight_pin=disp_blk)
'''
"""
# for 1.54" IPS 240x240 (RGB)
display = adafruit_st7789.ST7789(display_bus,
                                 width=240,
                                 height=240,
                                 rowstart=80,
                                 rotation=180,
                                 backlight_pin=disp_blk)
"""
"""
# for 2.0" IPS 240(RGB)x320
display = adafruit_st7789.ST7789(display_bus,
                                 width=240,
                                 height=320,
                                 backlight_pin=disp_blk)
"""
"""
# for 2.0" IPS 240(RGB)x320
# rotate 90 degree
disp_width = 240
disp_height = 320
display = adafruit_st7789.ST7789(display_bus,
                                 width=320,
                                 height=240,
                                 rotation=90,
                                 backlight_pin=disp_blk)
"""
#=======================================


splash = displayio.Group()
display.root_group = splash

def showGIF(gif):
    odg = gifio.OnDiskGif(gif)  # Create an OnDiskGif object with the given file.

    odg.next_frame() # Load the first frame

    face = displayio.TileGrid(
        odg.bitmap,
        pixel_shader=displayio.ColorConverter(
        input_colorspace=displayio.Colorspace.RGB565_SWAPPED
    ),
        x = int((display.width-odg.width)/2),
        y = int((display.height-odg.height)/2),
    )
    splash.append(face)
    display.refresh()

    for r in range(odg.frame_count-1):
        odg.next_frame() #load next frame
    splash.remove(face)


gifFiles = ("GIF/resized.gif")

while True:
    showGIF(gifFiles)
