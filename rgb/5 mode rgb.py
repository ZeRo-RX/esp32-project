from machine import Pin
from neopixel import NeoPixel
from time import sleep

rainbow = [(255 ,194 , 0),(255 ,0 , 0),(0 ,255 , 0),(0 ,0 , 255),(255 ,255 , 255),(23 ,131 , 146)]
x = 0

pixels = NeoPixel(Pin(2), 8)
while True:
  for i in range(8):
    pixels[i] = rainbow[x]
  pixels.write()
  sleep(1)
  x += 1
  if x == len(rainbow):
      x = 0
