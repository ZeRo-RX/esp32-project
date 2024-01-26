import time
from machine import Pin
import random

pt = Pin.OUT


PIN2 = Pin(2, pt)
PIN4 = Pin(4, pt)
PIN18 = Pin(18, pt)
PIN19 = Pin(19, pt)

numbers = [PIN2, PIN4, PIN18, PIN19]

while True:
    x = random.choice(numbers)# Write your code here :-)
    pinx = x
    pinx.on()
    time.sleep(0.1)
    pinx.off()
