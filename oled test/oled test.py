from machine import Pin, I2C
import OLED

pinsI2C = I2C(scl=Pin(5), sda=Pin(4))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)

oled.text('eee',10,10)
oled.show()
