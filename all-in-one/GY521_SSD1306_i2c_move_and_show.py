from machine import I2C, Pin, ADC, PWM
import mpu6050
import ssd1306
import time
import math

class SensorModule:
    def __init__(self):
        self.i2c = I2C(scl=Pin(22), sda=Pin(21))
        self.mpu = mpu6050.accel(self.i2c)
        self.oled = ssd1306.SSD1306_I2C(128, 64, self.i2c)
        self.adc1 = ADC(32)
        self.gyro_scale_factor = 1 / 131.072
        self.accel_scale_factor = 1 / 2.0

    def read_data(self):
        mpu_data = self.mpu.get_values()
        sensor_value1 = self.adc1.read()

        accel_x = mpu_data['AcX'] * self.accel_scale_factor
        accel_y = mpu_data['AcY'] * self.accel_scale_factor
        accel_z = mpu_data['AcZ'] * self.accel_scale_factor

        ax_degree = math.degrees(math.atan2(accel_x, accel_z))
        ay_degree = math.degrees(math.atan2(accel_y, accel_z))
        temperature = mpu_data['Tmp']

        return {
            'ax_degree': ax_degree,
            'ay_degree': ay_degree,
            'temperature': temperature,
            'sensor_value1': sensor_value1
        }

    def display_data(self, data):
        self.oled.fill(0)  # Clear the display

        self.oled.text('o', 60 - int(data['ay_degree']), 28 - int(data['ax_degree']))
        self.oled.text(f"T{data['temperature']:.0f}", 96, 0)
        self.oled.text(f"AX{data['ax_degree']:.0f}", 0, 0)
        self.oled.text(f"AY{data['ay_degree']:.0f}", 0, 10)
        self.oled.text(f"OUT:{data['sensor_value1']}", 0, 55)
        self.oled.show()