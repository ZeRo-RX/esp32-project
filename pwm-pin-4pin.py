import machine
import time

# تنظیم پارامترهای PWM
freq = 1000  # فرکانس PWM (هر ثانیه 1000 پالس)
duty_cycle = 512  # دوره کار (0 تا 1023)

# تنظیم پین‌ها برای استفاده از PWM
pin_numbers = [2, 4, 18, 19]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]
pwms = [machine.PWM(pin, freq=freq, duty=duty_cycle) for pin in pins]

try:
    while True:
        # افزایش دوره کار به تدریج
        for dc in range(0, 1024, 10):
            for pwm in pwms:
                pwm.duty(dc)
            time.sleep(0.005)

        # کاهش دوره کار به تدریج
        for dc in range(1023, -1, -10):
            for pwm in pwms:
                pwm.duty(dc)
            time.sleep(0.005)

except KeyboardInterrupt:
    # در صورت فشرده شدن Ctrl+C
    for pwm in pwms:
        pwm.deinit()  # آزاد کردن منابع PWM
    for pin in pins:
        pin.off()  # خاموش کردن پین‌ها
