from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import framebuf
import utime
import os


i2c = I2C(0, scl = Pin(9), sda = Pin(8), freq=400000)

display = SSD1306_I2C(128, 64, i2c)

display.fill(0)
display.show()

counter = 1
# get max number of frames in gif
frame_max = len(os.listdir("frames/"))

while True:
    #loop back to start
    if counter == frame_max:
        counter = 1
    
    filename = "frames/"+str(counter)+".pbm"
    
    with open(filename, 'rb') as f:
        #skip first line
        f.readline()
        #get image dimensions
        dims = f.readline().strip().split() # Dimensions
        x = int(dims[0])
        y = int(dims[1])
        #read image data
        data = bytearray(f.read())
        
    fbuf = framebuf.FrameBuffer(data, x, y, framebuf.MONO_HLSB)

    display.invert(1)
    display.blit(fbuf, 0, 0)
    display.show()
    counter += 1



