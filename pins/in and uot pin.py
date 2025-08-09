from machine import Pin
from time import sleep

led1 = Pin(2, Pin.OUT)
led2 = Pin(4, Pin.OUT)
led3 = Pin(16, Pin.OUT)
led4 = Pin(17, Pin.OUT)
relled = Pin(5, Pin.OUT)
rel1 = Pin(26, Pin.OUT)
rel2 = Pin(25, Pin.OUT)

pin13 = Pin(13, Pin.IN,Pin.PULL_UP)
pin12 = Pin(12, Pin.IN,Pin.PULL_UP)
pin14 = Pin(14, Pin.IN,Pin.PULL_UP)
pin27 = Pin(27, Pin.IN,Pin.PULL_UP)
while True:
    if pin13.value()==0:
        led1.on()
    else:
        led1.off()

    if pin12.value()==0:
        led2.on()
    else:
        led2.off()

    if pin14.value()==0:
        led3.on()
    else:
        led3.off()

    if pin27.value()==0:
        led4.on()
    else:
        led4.off()
    if pin13.value()==0 and pin12.value()==0 and pin14.value()==0 and pin27.value()==0:
        rel1.on()
        rel2.on()
    else:
        rel1.off()
        rel2.off()
    sleep(0.1)



