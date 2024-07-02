from machine import Pin
from neopixel import NeoPixel
from time import sleep

pixels = NeoPixel(Pin(2), 25)
pix = [1,3,5,7,9,11,13,17]
pix1 = [0,2,4,6,8,10,14,15,18]
rainbow = [
  (10 , 0 , 10),(40 , 0 , 20),(70 , 0 , 35),(100 , 0 , 50),(130 , 0 , 65),(100 , 0 , 50),(70 , 0 , 35),(40 , 0 , 20),(10 , 0 , 5)]
m = 0
while True:
    rainbow = rainbow[-1:] + rainbow[:-1]
    for i in pix:
        pixels[i] = rainbow[(m+1)]
    pixels.write()
    sleep(0.1)
