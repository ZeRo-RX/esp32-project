from machine import Pin


# تنظیم پین 14 به عنوان ورودی پول آپ
pin14 = Pin(14, Pin.IN, Pin.PULL_UP)

while True:
    # خواندن مقدار پین 14
    pin_value = pin14.value()

    # نمایش مقدار پین 14
    print("Pin 14 value:", pin_value)

    # تاخیر 1 ثانیه‌ای
    time.sleep(1)
