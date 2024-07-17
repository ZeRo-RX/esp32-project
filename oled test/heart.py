from machine import Pin, I2C
import OLED
# تنظیم I2C و OLED
pinsI2C = I2C(-1, Pin(22), Pin(21))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)

for x in range(0,16):
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
        oled.pixel(c,a,1)
        oled.pixel(a,a,1)
        oled.pixel(c2,a2,1)
        oled.pixel(a2,a2,1)
        oled.pixel(x2,e,1)
        oled.pixel(x4,w1,1)
        oled.pixel(x5,w1,1)
        oled.show()
        oled.pixel(x3,e,1)
        oled.show()
