from machine import Pin, I2C
import OLED

class OLEDDisplay:
    def __init__(self, width=128, height=64, scl_pin=22, sda_pin=21, i2c_freq=400000):
        self.width = width
        self.height = height
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.oled = OLED.SSD1306_I2C(width, height, self.i2c)
        self.oled.fill(0)
        self.oled.show()

    def draw_square(self, x, y, side_length):
        if x < 0 or y < 0 or x + side_length > self.width or y + side_length > self.height:
            raise ValueError("Square dimensions are out of bounds.")

        for i in range(side_length):
            self.oled.pixel(x + i, y, 1)
            self.oled.pixel(x + i, y + side_length - 1, 1)
            self.oled.pixel(x, y + i, 1)
            self.oled.pixel(x + side_length - 1, y + i, 1)

        self.oled.show()

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

# استفاده از کلاس برای نمایش یک مربع
oled_display = OLEDDisplay()

# پاک کردن صفحه نمایش
oled_display.clear()

# رسم مربع با طول ضلع 20 پیکسل در مختصات (10, 10)
oled_display.draw_square(10, 30, 20)
