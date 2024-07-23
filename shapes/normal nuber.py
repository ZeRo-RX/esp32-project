from machine import Pin, I2C
import OLED
import framebuf

class OLEDDisplay:
    def __init__(self, width=128, height=64, scl_pin=22, sda_pin=21, i2c_freq=400000):
        self.width = width
        self.height = height
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.oled = OLED.SSD1306_I2C(width, height, self.i2c)
        self.oled.fill(0)
        self.oled.show()

    def draw_large_digit(self, digit, x, y):
        font = [
            [0x1F, 0x11, 0x11, 0x11, 0x1F],  # 0
            [0x00, 0x00, 0x1F, 0x00, 0x00],  # 1
            [0x1D, 0x15, 0x15, 0x15, 0x17],  # 2
            [0x11, 0x15, 0x15, 0x15, 0x1F],  # 3
            [0x07, 0x04, 0x04, 0x1F, 0x04],  # 4
            [0x17, 0x15, 0x15, 0x15, 0x1D],  # 5
            [0x1F, 0x15, 0x15, 0x15, 0x1D],  # 6
            [0x01, 0x01, 0x01, 0x01, 0x1F],  # 7
            [0x1F, 0x15, 0x15, 0x15, 0x1F],  # 8
            [0x17, 0x15, 0x15, 0x15, 0x1F],  # 9
        ]

        for col in range(5):
            for row in range(7):
                pixel = (font[digit][col] >> row) & 0x01
                self.oled.pixel(x + col, y + row, pixel)
        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

# استفاده از کلاس برای نمایش اعداد بزرگ
oled_display = OLEDDisplay()

# پاک کردن صفحه نمایش
oled_display.clear()

# رسم عدد بزرگ 3 در موقعیت (10، 10)
oled_display.draw_large_digit(3, 10, 10)

# رسم عدد بزرگ 8 در موقعیت (20، 10)
oled_display.draw_large_digit(8, 20, 10)
