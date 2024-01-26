import time
import machine
import random

pin_numbers = [2, 4, 18, 19]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]

while True:
    x = random.choice(pins)
    pinx = x
    pinx.on()
    time.sleep(0.1)
    pinx.off()
