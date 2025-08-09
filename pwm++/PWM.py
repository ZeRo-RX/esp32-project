import machine
import time

pin = machine.Pin(2, machine.Pin.OUT)
pwm = machine.PWM(pin,freq=250000)

duty = 70
pwm.duty(duty)
