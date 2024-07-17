from machine import Pin, PWM 
import time

# پایه های ورودی
input1 = Pin(25, Pin.IN)
input2 = Pin(26, Pin.IN)
input3 = Pin(27, Pin.IN)

# پایه های خروجی
output1 = Pin(33, Pin.OUT)
output2 = Pin(15, Pin.OUT)
output3 = Pin(23, Pin.OUT)

# متغیرهای pwm
pwm1 = 0
pwm4 = 0
pwm5 = 0

# تنظیم PWM
pwm = PWM(Pin(33, Pin.OUT), freq=5000, duty=pwm1)

pwm2 = PWM(Pin(15, Pin.OUT), freq=5000, duty=pwm4)

pwm3 = PWM(Pin(23, Pin.OUT), freq=5000, duty=pwm5)

x1 = 51
x2 = 51
x3 = 51
while True:
    # خواندن مقادیر ورودی
    sw1 = input1.value()
    sw2 = input2.value()
    sw3 = input3.value()

    if sw1 == 1:
        pwm1 += x1
        if pwm1 >= 1020:
            x1 = -51
        if pwm1 <= 0:
            x1 = 51
        pwm.duty(pwm1)
    else:
        pass
    if sw2 == 1:
        pwm4 += x2
        if pwm4 >= 1020:
            x2 = -51
        if pwm4 <= 0:
            x2 = 51
        pwm2.duty(pwm4)
    else:
        pass
    if sw3 == 1:
        pwm5 += x3
        if pwm5 >= 1020:
            x3 = -51
        if pwm5 <= 0:
            x3 = 51
        pwm3.duty(pwm5)
    else:
        pass
    time.sleep(0.1)

    