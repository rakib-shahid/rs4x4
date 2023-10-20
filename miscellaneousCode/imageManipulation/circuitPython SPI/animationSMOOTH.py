import os, sys
import board
import busio
import terminalio
import displayio

import board
import neopixel
import struct


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
display.auto_refresh = False
splash = displayio.Group()
display.root_group = splash

gifFiles = ("GIF/resizedOG.gif")
odg = gifio.OnDiskGif(gifFiles)

start = time.monotonic()
next_delay = odg.next_frame() # Load the first frame
end = time.monotonic()
overhead = end - start

while True:
    # time.sleep(min(0, next_delay - overhead))
    time.sleep(0)
    next_delay = odg.next_frame()

    display_bus.send(42, struct.pack(">hh", 0, odg.bitmap.width - 1))
    display_bus.send(43, struct.pack(">hh", 0, odg.bitmap.height - 1))
    display_bus.send(44, odg.bitmap)


