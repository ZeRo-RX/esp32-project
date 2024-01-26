from machine import Pin, PWM
import time

class PWMManager:
    def __init__(self, pins, freq=1000, duty_cycle=512):
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.pins = pins
        self.pwms = [PWM(Pin(pin), freq=freq, duty=duty_cycle) for pin in pins]

    def increase_pwm_duty(self, step=10, sleep_time=0.005):
        for dc in range(0, 1024, step):
            for pwm in self.pwms:
                pwm.duty(dc)
            time.sleep(sleep_time)

    def decrease_pwm_duty(self, step=10, sleep_time=0.005):
        for dc in range(1023, -1, -step):
            for pwm in self.pwms:
                pwm.duty(dc)
            time.sleep(sleep_time)

    def cleanup(self):
        for pwm in self.pwms:
            pwm.deinit()  # آزاد کردن منابع PWM
        for pin in self.pins:
            Pin(pin, Pin.OUT).off()  # خاموش کردن پین‌ها
