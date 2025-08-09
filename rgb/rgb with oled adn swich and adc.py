from machine import Pin,I2C,ADC
from neopixel import NeoPixel
from time import sleep
import OLED

rgb = NeoPixel(Pin(1), 8)

pinsI2C = I2C(scl=Pin(9), sda=Pin(8))
oled = OLED.SSD1306_I2C(128, 64, pinsI2C)

sw = Pin(3, Pin.IN, Pin.PULL_DOWN)
VL = ADC(2)
VL.atten(ADC.ATTN_11DB)
r = 0
g = 0
b = 0
s = 0
while True:
    vsw = sw.value()
    VVL = VL.read()
    oled.text('R',20,25)
    oled.text('G',60,25)
    oled.text('B',100,25)
    oled.text(f'{r}',12,45,1)
    oled.text(f'{g}',52,45,1)
    oled.text(f'{b}',92,45,1)
    oled.show()
    oled.text(f'{r}',12,45,0)
    oled.text(f'{g}',52,45,0)
    oled.text(f'{b}',92,45,0)
    
    if vsw == 1:
        s += 1
        if s > 3:
            s = 0
    if s == 0:
        for i in range(8):
            rgb[i] = (0,0,0)
        rgb.write()
    if s == 1:
        r = int(VVL/16)
        for i in range(20):
            oled.pixel(13+i,18,1)
            oled.pixel(13+i,38,1)
            oled.pixel(13,18+i,1)
            oled.pixel(33,18+i,1)
            for i in range(8):
                rgb[i] = (r,g,b)
            rgb.write()
    else:
        for i in range(20):
            oled.pixel(13+i,18,0)
            oled.pixel(13+i,38,0)
            oled.pixel(13,18+i,0)
            oled.pixel(33,18+i,0)
    
    if s == 2:
        g = int(VVL/16)
        for i in range(20):
            oled.pixel(53+i,18,1)
            oled.pixel(53+i,38,1)
            oled.pixel(53,18+i,1)
            oled.pixel(73,18+i,1)
            for i in range(8):
                rgb[i] = (r,g,b)
            rgb.write()
    else:
        for i in range(20):
            oled.pixel(53+i,18,0)
            oled.pixel(53+i,38,0)
            oled.pixel(53,18+i,0)
            oled.pixel(73,18+i,0)
        
    if s == 3:
        b = int(VVL/16)
        for i in range(20):
            oled.pixel(93+i,18,1)
            oled.pixel(93+i,38,1)
            oled.pixel(93,18+i,1)
            oled.pixel(113,18+i,1)
            for i in range(8):
                rgb[i] = (r,g,b)
            rgb.write()
    else:
        for i in range(20):
            oled.pixel(93+i,18,0)
            oled.pixel(93+i,38,0)
            oled.pixel(93,18+i,0)
            oled.pixel(113,18+i,0)
                 
    sleep(0.05)