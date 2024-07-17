from machine import Pin , I2C
import OLED
import time
import random

pinsI2C = I2C(-1,Pin(22),Pin(21))
oled = OLED.SSD1306_I2C(128,64,pinsI2C)
x = 0
a = 15
counter = 0
while True:
    x = random.randrange(0,120)
    y = random.randrange(0,55)
    oled.text('O', x, y)
    oled.show()
    time.sleep(0.07)
    oled.fill(0)
