import os, sys
import board
import busio
import terminalio
import displayio

import board
import neopixel


import adafruit_st7789
from adafruit_st7735r import ST7735R
import time
import gifio

# Release any resources currently in use for the displays
displayio.release_displays()

mosi_pin = board.GP11
clk_pin = board.GP10
reset_pin = board.GP17
cs_pin = board.GP18
dc_pin = board.GP16

pixel_pin = board.GP23
num_pixels = 1

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)


#===init display ======================
disp_blk = board.LED
disp_cs  = board.GP18
disp_dc  = board.GP16
disp_res = board.GP17

disp_mosi = board.GP11
disp_clk = board.GP10

spi = busio.SPI(clock=clk_pin, MOSI=mosi_pin)

display_bus = displayio.FourWire(spi, command=dc_pin, chip_select=cs_pin, reset=reset_pin)

display = ST7735R(display_bus, width=130, height=161, bgr = True)

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
    display.refresh(minimum_frames_per_second=60)

    for r in range(odg.frame_count-1):
        odg.next_frame() #load next frame
        
    splash.remove(face)

gifFiles = ("GIF/idekatp.gif")

while True:
    pixels.fill((255, 0, 0))
    pixels.show()
    showGIF(gifFiles)

