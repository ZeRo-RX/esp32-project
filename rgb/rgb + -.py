from machine import Pin
from neopixel import NeoPixel
from time import sleep

r = 2
g = 12
b = 255
xx = 0
x = 0.1
increasing = True
pixels = NeoPixel(Pin(2), 8)

while True:
    for i in range(8):
        R = int(r / x)
        G = int(g / x)
        B = int(b / x)

        # بررسی مقادیر برای جلوگیری از تجاوز از حد مجاز
        if R > r:
            R = r
        if G > g:
            G = g
        if B > b:
            B = b

        pixels[i] = (R, G, B)

    print(R, G, B)
    pixels.write()
    sleep(0.1)  # کاهش زمان خواب برای بهبود انیمیشن

    # مدیریت روند افزایشی و کاهشی
    if increasing:  # اگر روند افزایشی باشد
        xx = x**0.3
    else:  # اگر روند کاهشی باشد
        xx = -(x**0.1)  # اصلاح مقدار کاهشی برای موثرتر بودن

    x += xx  # به‌روزرسانی مقدار x
    if x < 0.1:  # جلوگیری از تقسیم بر صفر یا مقادیر منفی
        x = 0.1

    print(f"x: {x}, xx: {xx}")

    # تغییر حالت در نقاط کلیدی
    if increasing and x >= 50:  # وقتی x به 50 برسد
        increasing = False  # تغییر به حالت کاهشی
    elif not increasing and x <= 0.1:  # وقتی x به حداقل مقدار برسد
        increasing = True  # تغییر به حالت افزایشی
