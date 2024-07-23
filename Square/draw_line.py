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

    def draw_triangle(self, x1, y1, x2, y2, x3, y3):
        self._draw_line(x1, y1, x2, y2)
        self._draw_line(x2, y2, x3, y3)
        self._draw_line(x3, y3, x1, y1)
        self.oled.show()

    def draw_circle(self, x0, y0, radius):
        x = radius
        y = 0
        err = 0

        while x >= y:
            self.oled.pixel(x0 + x, y0 + y, 1)
            self.oled.pixel(x0 + y, y0 + x, 1)
            self.oled.pixel(x0 - y, y0 + x, 1)
            self.oled.pixel(x0 - x, y0 + y, 1)
            self.oled.pixel(x0 - x, y0 - y, 1)
            self.oled.pixel(x0 - y, y0 - x, 1)
            self.oled.pixel(x0 + y, y0 - x, 1)
            self.oled.pixel(x0 + x, y0 - y, 1)
            y += 1
            if err <= 0:
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

        self.oled.show()

    def _draw_line(self, x1, y1, x2, y2):
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.oled.pixel(x1, y1, 1)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

# استفاده از کلاس برای نمایش یک دایره
oled_display = OLEDDisplay()

# پاک کردن صفحه نمایش
oled_display.clear()

# رسم دایره با شعاع 20 پیکسل در مختصات (30, 30)
oled_display.draw_circle(30, 30, 40)
