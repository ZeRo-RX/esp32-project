from machine import Pin, I2C
import OLED
import math

class OLEDDisplay:
    def __init__(self, width=128, height=64, scl_pin=22, sda_pin=21, i2c_freq=400000):
        self.width = width
        self.height = height
        self.i2c = I2C(0, scl=Pin(scl_pin), sda=Pin(sda_pin), freq=i2c_freq)
        self.oled = OLED.SSD1306_I2C(width, height, self.i2c)
        self.oled.fill(0)
        self.oled.show()
        self.last_hand_coords = None

    def draw_square(self, x, y, side_length, filled=False):
        if x < 0 or y < 0 or x + side_length > self.width or y + side_length > self.height:
            raise ValueError("Square dimensions are out of bounds.")

        if filled:
            for i in range(side_length):
                for j in range(side_length):
                    self.oled.pixel(x + i, y + j, 1)
        else:
            for i in range(side_length):
                self.oled.pixel(x + i, y, 1)
                self.oled.pixel(x + i, y + side_length - 1, 1)
                self.oled.pixel(x, y + i, 1)
                self.oled.pixel(x + side_length - 1, y + i, 1)

        self.oled.show()

    def draw_triangle(self, x1, y1, x2, y2, x3, y3, filled=False):
        if filled:
            self._fill_triangle(x1, y1, x2, y2, x3, y3)
        else:
            self._draw_line(x1, y1, x2, y2)
            self._draw_line(x2, y2, x3, y3)
            self._draw_line(x3, y3, x1, y1)
        self.oled.show()

    def draw_circle(self, x0, y0, radius, filled=False):
        x = radius
        y = 0
        err = 0

        if filled:
            while x >= y:
                self._draw_filled_circle_lines(x0, y0, x, y)
                y += 1
                if err <= 0:
                    err += 2 * y + 1
                if err > 0:
                    x -= 1
                    err -= 2 * x + 1
        else:
            while x >= y:
                self._draw_circle_points(x0, y0, x, y)
                y += 1
                if err <= 0:
                    err += 2 * y + 1
                if err > 0:
                    x -= 1
                    err -= 2 * x + 1

        self.oled.show()

    def draw_ellipse(self, x0, y0, a, b, filled=False):
        x = -a
        y = 0
        err = 2 - 2 * a
        b2 = b * b
        a2 = a * a

        if filled:
            while x <= 0:
                self._draw_filled_ellipse_lines(x0, y0, x, y)
                e2 = err
                if e2 <= y:
                    y += 1
                    err += y * 2 + 1
                if e2 > x or err > y:
                    x += 1
                    err += x * 2 + 1
        else:
            while x <= 0:
                self._draw_ellipse_points(x0, y0, x, y)
                e2 = err
                if e2 <= y:
                    y += 1
                    err += y * 2 + 1
                if e2 > x or err > y:
                    x += 1
                    err += x * 2 + 1

        self.oled.show()

    def draw_hand(self, x0, y0, radius, angle_degrees):
        angle_radians = math.radians(angle_degrees)
        x1 = x0 + int(radius * math.cos(angle_radians))
        y1 = y0 - int(radius * math.sin(angle_radians))
        self._draw_line(x0, y0, x1, y1)
        self.oled.show()
        self.last_hand_coords = (x0, y0, x1, y1)

    def _draw_line(self, x1, y1, x2, y2, color=1):
        # Bresenham's line algorithm
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.oled.pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_moving_hand(self, x0, y0, radius, angle_degrees):
        if self.last_hand_coords:
            x1, y1, x2, y2 = self.last_hand_coords
            self._draw_line(x1, y1, x2, y2, color=0)  # Erase the previous hand

        self.draw_hand(x0, y0, radius, angle_degrees)

    def _fill_triangle(self, x1, y1, x2, y2, x3, y3):
        def draw_line_low(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            yi = 1 if dy > 0 else -1
            dy = abs(dy)
            D = 2*dy - dx
            y = y0

            for x in range(x0, x1+1):
                self.oled.pixel(x, y, 1)
                if D > 0:
                    y = y + yi
                    D = D - 2*dx
                D = D + 2*dy

        def draw_line_high(x0, y0, x1, y1):
            dx = x1 - x0
            dy = y1 - y0
            xi = 1 if dx > 0 else -1
            dx = abs(dx)
            D = 2*dx - dy
            x = x0

            for y in range(y0, y1+1):
                self.oled.pixel(x, y, 1)
                if D > 0:
                    x = x + xi
                    D = D - 2*dy
                D = D + 2*dx

        def fill_flat_bottom_triangle(v1, v2, v3):
            slope1 = (v2[0] - v1[0]) / (v2[1] - v1[1])
            slope2 = (v3[0] - v1[0]) / (v3[1] - v1[1])

            curx1 = v1[0]
            curx2 = v1[0]

            for scanlineY in range(v1[1], v2[1] + 1):
                draw_line_low(int(curx1), scanlineY, int(curx2), scanlineY)
                curx1 += slope1
                curx2 += slope2

        def fill_flat_top_triangle(v1, v2, v3):
            slope1 = (v3[0] - v1[0]) / (v3[1] - v1[1])
            slope2 = (v3[0] - v2[0]) / (v3[1] - v2[1])

            curx1 = v3[0]
            curx2 = v3[0]

            for scanlineY in range(v3[1], v1[1] - 1, -1):
                draw_line_low(int(curx1), scanlineY, int(curx2), scanlineY)
                curx1 -= slope1
                curx2 -= slope2

        # Sort vertices by y-coordinate ascending (v1, v2, v3)
        vertices = sorted([(x1, y1), (x2, y2), (x3, y3)], key=lambda v: v[1])

        # Extract sorted vertices
        v1, v2, v3 = vertices

        # Check for flat-bottom triangle
        if v2[1] == v3[1]:
            fill_flat_bottom_triangle(v1, v2, v3)
        # Check for flat-top triangle
        elif v1[1] == v2[1]:
            fill_flat_top_triangle(v1, v2, v3)
        else:
            # General case: split the triangle into a flat-bottom and flat-top
            v4 = (int(v1[0] + ((v2[1] - v1[1]) / float(v3[1] - v1[1])) * (v3[0] - v1[0])), v2[1])
            fill_flat_bottom_triangle(v1, v2, v4)
            fill_flat_top_triangle(v2, v4, v3)

    def _draw_circle_points(self, x0, y0, x, y):
        self.oled.pixel(x0 + x, y0 + y, 1)
        self.oled.pixel(x0 + y, y0 + x, 1)
        self.oled.pixel(x0 - y, y0 + x, 1)
        self.oled.pixel(x0 - x, y0 + y, 1)
        self.oled.pixel(x0 - x, y0 - y, 1)
        self.oled.pixel(x0 - y, y0 - x, 1)
        self.oled.pixel(x0 + y, y0 - x, 1)
        self.oled.pixel(x0 + x, y0 - y, 1)

    def _draw_filled_circle_lines(self, x0, y0, x, y):
        self._draw_line(x0 - x, y0 + y, x0 + x, y0 + y)
        self._draw_line(x0 - y, y0 + x, x0 + y, y0 + x)
        self._draw_line(x0 - x, y0 - y, x0 + x, y0 - y)
        self._draw_line(x0 - y, y0 - x, x0 + y, y0 - x)

    def _draw_ellipse_points(self, x0, y0, x, y):
        self.oled.pixel(x0 - x, y0 + y, 1)
        self.oled.pixel(x0 + x, y0 + y, 1)
        self.oled.pixel(x0 + x, y0 - y, 1)
        self.oled.pixel(x0 - x, y0 - y, 1)

    def _draw_filled_ellipse_lines(self, x0, y0, x, y):
        self._draw_line(x0 - x, y0 + y, x0 + x, y0 + y)
        self._draw_line(x0 - x, y0 - y, x0 + x, y0 - y)

    def clear(self):
        self.oled.fill(0)
        self.oled.show()

# استفاده از کلاس برای نمایش اشکال و عقربه ساعت
oled_display = OLEDDisplay()

# پاک کردن صفحه نمایش
oled_display.clear()

# رسم دایره توپر با شعاع 30 در مرکز (64, 32)
oled_display.draw_circle(64, 32, 30, )

# رسم عقربه ساعت در زاویه 45 درجه
oled_display.draw_moving_hand(64, 32, 30, 45)

#برای تغییر زاویه عقربه، دوباره از متد draw_moving_hand استفاده کنید
oled_display.draw_moving_hand(64, 32, 30, 90)

while True:
    for i in range(360):
        oled_display.draw_moving_hand(64, 32, 28, i)
        oled_display.draw_moving_hand(64, 32, 60, -i)
    oled_display.draw_circle(64, 32, 30, )

