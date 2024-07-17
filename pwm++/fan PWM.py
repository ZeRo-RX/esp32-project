import machine
import time

# تنظیم پین GPIO2 به عنوان خروجی PWM
pin = machine.Pin(2, machine.Pin.OUT)

# تنظیم فرکانس PWM به 25 کیلو هرتز
pwm = machine.PWM(pin, freq=25000)

# تنظیم وظیفه PWM به 50%
duty = 50
pwm.duty(duty)

# حلقه برای 10 ثانیه
for i in range(10):
  # وظیفه PWM را به طور خطی از 0% به 100% و سپس از 100% به 0% تغییر دهید
  for duty in range(0, 1001):
    pwm.duty(duty)
    time.sleep_ms(50)
  for duty in range(100, -100, -100):
    pwm.duty(duty)
    time.sleep_ms(50)

# پاکسازی PWM
pwm.deinit()
