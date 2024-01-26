import time
from machine import Pin
import random

pt = Pin.OUT


PIN2 = Pin(2, pt)
PIN4 = Pin(4, pt)
PIN18 = Pin(18, pt)
PIN19 = Pin(19, pt)
PIN16 = Pin(16, pt)
PIN17 = Pin(17, pt)
PIN5 = Pin(5, pt)
PIN21 = Pin(21, pt)

numbers = [PIN2, PIN4, PIN18, PIN19,PIN16,PIN17,PIN5,PIN21]

while True:
    x = random.choice(numbers)# Write your code here :-)
    pinx = x
    pinx.on()
    time.sleep(0.1)
    pinx.off()
