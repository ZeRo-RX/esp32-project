from machine import Pin
from neopixel import NeoPixel
from time import sleep

rgb = NeoPixel(Pin(2),8)

while True:
    for i in range(1,9):
        rgb[i-1] = (50,0,255)
        rgb[i-2] = (0,0,0)
        sleep(0.1)
        rgb.write()
    for i in range(1,9):
        rgb[7-i] = (50,0,255)
        rgb[8-i] = (0,0,0)
        sleep(0.1)
        rgb.write()
