from machine import Pin
from neopixel import NeoPixel
from time import sleep

rainbow = (125 ,0 , 255)

pixels = NeoPixel(Pin(4), 25)
while True:
  for i in range(25):
    pixels[i] = rainbow
  pixels.write()
  sleep(0.01)
