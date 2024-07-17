from machine import Pin, I2C
import OLED
from neopixel import NeoPixel
from time import sleep

pix = NeoPixel(Pin(4), 25)

i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = OLED.SSD1306_I2C(128, 64, i2c)

sw1 = Pin(15, Pin.IN, Pin.PULL_DOWN)
sw2 = Pin(5, Pin.IN, Pin.PULL_DOWN)
sw3 = Pin(18, Pin.IN, Pin.PULL_DOWN)

pixh = [3,5,7,11,13,15,17,23]
pp = [3,5,7,11,13,15,17,23]

rainbowh = [
  (2 , 0 , 1),(10 , 0 , 5),(40 , 0 , 35),(70 , 0 , 65),(100 ,0 , 95),(130 , 0 , 125),(100 , 0 , 95),(70 , 0 , 65),(40 , 0 , 35),(10 , 0 , 5),(2 , 0 , 1)]

rainbow = [
  (126 , 1 , 0),(114 , 13 , 0),(102 , 25 , 0),(90 , 37 , 0),(78 , 49 , 0),(66 , 61 , 0),(54 , 73 , 0),(42 , 85 , 0),
  (30 , 97 , 0),(18 , 109 , 0),(6 , 121 , 0),(0 , 122 , 5),(0 , 110 , 17),(0 , 98 , 29),(0 , 86 , 41),(0 , 74 , 53),
  (0 , 62 , 65),(0 , 50 , 77),(0 , 38 , 89),(0 , 26 , 101),(0 , 14 , 113),(0 , 2 , 125),(9 , 0 , 118),(21 , 0 , 106),
  (33 , 0 , 94),(45 , 0 , 82),(57 , 0 , 70),(69 , 0 , 58),(81 , 0 , 46),(93 , 0 , 34),(105 , 0 , 22),(117 , 0 , 10)]

pi = 25
xx = 0
x = 0
y = 0
yy = 0
m = 0
while True:
    if sw1.value() == 1:
        if sw2.value() == 1:
            x += 1
            if x == 10:
                x = 1
            sleep(0.18)

        if sw3.value() == 0:
            y += yy
            if y >= 250:
                yy -= 25
            if y <= 0:
                yy += 25
            sleep(0.18)

        if x == 1:
            for i in range(pi):
                pix[i] = (0,int(255-y),0)
            oled.fill(0)
            oled.text("Green", 45, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        elif x == 2:
            for i in range(pi):
                pix[i] = (int(255-y),0,0)
            oled.fill(0)
            oled.text("Red", 45, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        elif x == 3:
            for i in range(pi):
                pix[i] = (0,0,int(255-y))
            oled.fill(0)
            oled.text("Blue", 45, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        elif x == 4:
            for i in range(pi):
                pix[i] = (int(255-y),0,int(255-y))
            oled.fill(0)
            oled.text("red and pink", 20, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        elif x == 5:
            for i in range(pi):
                pix[i] = (0,int(255-y),int(255-y))
            oled.fill(0)
            oled.text("Cyan", 45, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        elif x == 6:
            for i in range(pi):
                pix[i] = (int(255-y),int(255-y),0)
            oled.fill(0)
            oled.text("yellow", 35, 30)
            oled.show()
            pix.write()
            sleep(0.05)

        while x == 7:
            rainbow = rainbow[-1:] + rainbow[:-1]
            for i in range(pi):
                pix[i] = rainbow[i]
            oled.fill(0)
            oled.text("rainbow", 35, 30)
            oled.show()
            pix.write()
            sleep(0.05)
            if sw2.value() == 1:
                break
            elif sw1.value() == 0:
                break

        if x == 8:
            while True:
                rainbow = rainbow[-1:] + rainbow[:-1]
                for i in range(pi):
                    pix[i] = (0 , 0 , 0)
                oled.fill(0)
                oled.text("off", 45, 30)
                oled.show()
                pix.write()
                sleep(0.03)
                if sw2.value() == 1 or sw1.value() == 0:
                    break

        elif x == 9:
            oled.fill(0)
            for xx in range(0,16):
                a = 63 - xx
                a2 = 47 - xx
                x2 = xx + 32
                x3 = xx + 64
                x4 = xx + 80
                x5 = xx + 48
                c = xx + 64
                c2 = xx + 80
                b = 32 + xx
                e = a - 32
                w = 0 + xx
                w1 = 16 + xx
                oled.pixel(c,a,1)
                oled.pixel(a,a,1)
                oled.pixel(c2,a2,1)
                oled.pixel(a2,a2,1)
                oled.pixel(x2,e,1)
                oled.pixel(x4,w1,1)
                oled.pixel(x5,w1,1)
                oled.text("Heart", 45, 30)
                oled.show()
                oled.pixel(x3,e,1)
                oled.show()
            while True:
                rainbowh = rainbowh[-1:] + rainbowh[:-1]
                for i in range(len(pixh)):
                    pix[pixh[i]] = rainbowh[m % len(rainbowh)]
                pix.write()
                sleep(0.03)
                if sw2.value() == 1 or sw1.value() == 0:
                    break
                m += 1

    elif sw1.value() == 0:
        x = 0
        if x == 0:
            for i in range(pi):
                pix[i] = (0,0,0)
            oled.fill(0)
            oled.show()
            pix.write()
            sleep(0.03)

