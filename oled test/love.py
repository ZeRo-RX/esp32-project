from machine import Pin, I2C
import OLED
import time

mx = 0
mm = 0

# تنظیم I2C و OLED
pinsI2C = I2C(-1, Pin(22), Pin(21))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)

# تابع نمایش
def display():
    for x in range(0, 16):
        a = 63 - x
        a2 = 47 - x
        x2 = x + 32
        x3 = x + 64
        x4 = x + 80
        x5 = x + 48
        c = x + 64
        c2 = x + 80
        b = 32 + x
        e = a - 32
        w = 0 + x
        w1 = 16 + x

        oled.pixel(c, a, 1)
        oled.pixel(a, a, 1)
        oled.pixel(c2, a2, 1)
        oled.pixel(a2, a2, 1)
        oled.pixel(x2, e, 1)
        oled.pixel(x4, w1, 1)
        oled.pixel(x5, w1, 1)
        oled.pixel(x3, e, 1)
        oled.pixel(x3, e - 1, 1)
        oled.show()

# اجرای تابع نمایش
display()



mm = 1# حلقه نمایش نقاط
for p in range(0,288):
    mx += 1
    ma = 63 - mx
    ma2 = 47 - mx
    mx2 = mx + 32
    mx3 = mx + 64
    mx4 = mx + 80
    mx5 = mx + 48
    mc = mx + 64
    mc2 = mx + 80
    mb = 32 + mx
    me = ma - 32
    mw = 0 + mx
    mw1 = 16 + mx
    if mx == 32:
        mx = 0
        mm += 1
    else:
        oled.pixel(ma+mm, ma-mm, 1)
        oled.pixel(mx5-1-mm, mw1-1+mm, 1)
        oled.pixel(mc+1-mm, ma-mm, 1)
        oled.pixel(mx3-7-mm, me +24 -mm, 1)
    oled.show()

