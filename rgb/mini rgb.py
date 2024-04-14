from machine import Pin
from neopixel import NeoPixel
from time import sleep

pi = 8

sw1 = Pin(13, Pin.IN,)
sw2 = Pin(5, Pin.IN, )
sw3 = Pin(4, Pin.IN,)

pixels1 = NeoPixel(Pin(14), pi)
pixels2 = NeoPixel(Pin(12), pi)

rainbow = [
  (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
  (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
  (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
  (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

x = 0
y = 0
yy = 0
while True:
    if sw1.value() == 1:
        if sw2.value() == 1:
            x += 1
            if x == 8:
                x = 1
            sleep(0.18)

        if sw3.value() == 1:
            y += yy
            if y >= 250:
                yy -= 25
            if y <= 0:
                yy += 25
            sleep(0.18)

        if x == 1:
            for i in range(pi):
                pixels1[i] = (0,int(255-y),0)
                pixels2[i] = (0,int(255-y),0)
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        elif x == 2:
            for i in range(pi):
                pixels1[i] = (int(255-y),0,0)
                pixels2[i] = (int(255-y),0,0)
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        elif x == 3:
            for i in range(pi):
                pixels1[i] = (0,0,int(255-y))
                pixels2[i] = (0,0,int(255-y))
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        elif x == 4:
            for i in range(pi):
                pixels1[i] = (int(255-y),0,int(255-y))
                pixels2[i] = (int(255-y),0,int(255-y))
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        elif x == 5:
            for i in range(pi):
                pixels1[i] = (0,int(255-y),int(255-y))
                pixels2[i] = (0,int(255-y),int(255-y))
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        elif x == 6:
            for i in range(pi):
                pixels1[i] = (int(255-y),int(255-y),0)
                pixels2[i] = (int(255-y),int(255-y),0)
            pixels1.write()
            pixels2.write()
            sleep(0.03)

        while x == 7:
            rainbow = rainbow[-1:] + rainbow[:-1]
            for i in range(pi):
                pixels1[i] = rainbow[i]
                pixels2[i] = rainbow[i]
            pixels1.write()
            pixels2.write()
            sleep(0.03)
            if sw2.value() == 1:
                break
            elif sw1.value() == 0:
                break

    elif sw1.value() == 0:
        x = 0
        if x == 0:
            for i in range(pi):
                pixels1[i] = (0,0,0)
                pixels2[i] = (0,0,0)
            pixels1.write()
            pixels2.write()
            sleep(0.03)
