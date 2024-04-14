from machine import Pin
from neopixel import NeoPixel
from time import sleep

pi = 8

sw1 = Pin(13, Pin.IN, Pin.PULL_DOWN)
sw2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
sw3 = Pin(4, Pin.IN, Pin.PULL_DOWN)

pixels1 = NeoPixel(Pin(14), pi)
pixels2 = NeoPixel(Pin(12), pi)

rainbow = [
  (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
  (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
  (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
  (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

gerin = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
pink = (255,0,255)
off = (0,0,0)

x = 0

if sw1 == 1:
    if sw2 == 1:
        x += 1
        if x == 6:
            x = 1
        else:

    if x == 2:
        for i in range(pi):
            pixels1[i] = (0,255,0)
            pixels2[i] = (0,255,0)
        pixels.write()
        sleep(0.03)

    elif x == 3:
        for i in range(pi):
            pixels1[i] = (255,0,0)
            pixels2[i] = (255,0,0)
        pixels.write()
        sleep(0.03)

    elif x == 4:
        for i in range(pi):
            pixels1[i] = (0,0,255)
            pixels2[i] = (0,0,255)
        pixels.write()
        sleep(0.03)

    elif x == 5:
        for i in range(pi):
            pixels1[i] = (255,0,255)
            pixels2[i] = (255,0,255)
        pixels.write()
        sleep(0.03)

elif sw1 == 0:
    x = 0
    if x == 0:
        for i in range(pi):
            pixels1[i] = (0,0,0)
            pixels2[i] = (0,0,0)
        pixels.write()
        sleep(0.03)



