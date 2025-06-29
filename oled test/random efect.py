from machine import Pin, I2C
import OLED
import random
import time

pinsI2C = I2C(0, scl=Pin(22), sda=Pin(21))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)

while True:
    for i in range(64):
        oled.pixel(127, i, 1)
        oled.scroll(-1, 0)
        oled.pixel(127, i - 1, 0)
        oled.show()
    oled.text("ooo",20,20)
    for i in range(64):
        oled.pixel(127, 63 - i, 1)
        oled.scroll(-1, 0)
        oled.pixel(127, 63 - i + 1, 0)
        oled.show()
