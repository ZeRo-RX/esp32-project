import machine
import time

# تنظیم پین GPIO2 به عنوان خروجی PWM
pin = machine.Pin(2, machine.Pin.OUT)

# تنظیم فرکانس PWM به 25 کیلو هرتز
pwm = machine.PWM(pin, freq=25000)

# تنظیم وظیفه PWM به 50%
duty = 50
pwm.duty(duty)
