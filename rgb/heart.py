from machine import Pin
from neopixel import NeoPixel
from time import sleep

pixels = NeoPixel(Pin(21), 25)
pix = [3,5,7,11,13,15,17,23]
pix1 = [0,2,4,6,8,10,14,15,18]
rainbow = [
  (2 , 0 , 1),(10 , 0 , 5),(40 , 0 , 35),(70 , 0 , 65),(100 ,0 , 95),(130 , 0 , 125),(100 , 0 , 95),(70 , 0 , 65),(40 , 0 , 35),(10 , 0 , 5),(2 , 0 , 1)]
m = 0
while True:
    rainbow = rainbow[-1:] + rainbow[:-1]
    for i in pix:
        pixels[i] = rainbow[(m+1)]
    pixels.write()
    sleep(0.1)
