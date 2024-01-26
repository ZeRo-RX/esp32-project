from machine import Pin, PWM
import utime

class PWMManager:
    def __init__(self, pins, freq=1024, duty_cycle=0):
        self.freq = freq
        self.duty_cycle = duty_cycle
        self.pins = pins
        self.pwms = [PWM(Pin(pin), freq=freq, duty=duty_cycle) for pin in pins]

    def run_pwm_sequence(self, step=10, sleep_time=10):
        for _ in range(10000000):  # تعداد دفعات تکرار
            for pwm in self.pwms:
                for dc in range(0, 1024, step):
                    pwm.duty(dc)
                    utime.sleep_ms(sleep_time)

            utime.sleep_ms(sleep_time)  # تاخیر قبل از خاموش کردن پایه‌ها

            for pwm in self.pwms:
                for dc in range(1023, -1, -step):
                    pwm.duty(dc)
                    utime.sleep_ms(sleep_time)

    def cleanup(self):
        for pwm in self.pwms:
            pwm.deinit()  # آزاد کردن منابع PWM
        for pin in self.pins:
            Pin(pin, Pin.OUT).off()  # خاموش کردن پین‌ها
