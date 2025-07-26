from machine import Pin
from time import sleep

# تعریف پین‌های LED و رله
led_pins = [Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]
relays = [Pin(26, Pin.OUT), Pin(25, Pin.OUT)]

# تعریف پین‌های ورودی با Pull-up فعال
input_pins = [Pin(13, Pin.IN, ), Pin(12, Pin.IN), Pin(14, Pin.IN), Pin(27, Pin.IN)]

while True:
    # چک کردن هر ورودی و کنترل LED‌های مربوطه
    all_pressed = True  # متغیر برای بررسی همه پین‌ها
    for i in range(4):
        if input_pins[i].value() == 0:
            led_pins[i].on()
        else:
            led_pins[i].off()
            all_pressed = False  # اگر هر پین آزاد باشد، این متغیر False می‌شود

    # کنترل رله‌ها براساس وضعیت پین‌ها
    if all_pressed:
        for relay in relays:
            relay.on()
    else:
        for relay in relays:
            relay.off()

    sleep(0.1)
