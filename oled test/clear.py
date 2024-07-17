# Write your code here :-)
from machine import Pin, I2C
import OLED

pinsI2C = I2C(-1, Pin(22), Pin(21))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)
oled.fill(0)
