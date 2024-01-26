import machine
import utime

# تنظیم پارامترهای PWM
freq = 1024  # فرکانس PWM (هر ثانیه 1000 پالس)
duty_cycle = 0  # دوره کار اولیه

# تنظیم پین‌ها برای استفاده از PWM
pin_numbers = [2, 4, 18, 19]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]
pwms = [machine.PWM(pin, freq=freq, duty=duty_cycle) for pin in pins]

try:
    for _ in range(10000000):  # تعداد دفعات تکرار
        for pwm in pwms:
            for dc in range(0, 1024, 10):
                pwm.duty(dc)
                utime.sleep_ms(10)

        utime.sleep_ms(10)  # تاخیر قبل از خاموش کردن پایه‌ها

        for pwm in pwms:
            for dc in range(1023, -1, -10):
                pwm.duty(dc)
                utime.sleep_ms(10)

except KeyboardInterrupt:
    # در صورت فشرده شدن Ctrl+C
    for pwm in pwms:
        pwm.deinit()  # آزاد کردن منابع PWM
    for pin in pins:
        pin.off()  # خاموش کردن پین‌ها
