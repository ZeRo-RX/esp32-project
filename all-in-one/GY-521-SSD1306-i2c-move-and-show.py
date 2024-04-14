from machine import I2C, Pin, ADC
import mpu6050
import ssd1306
import time
import math

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu = mpu6050.accel(i2c)
oled = ssd1306.SSD1306_I2C(128, 64, i2c)
adc1 = ADC(32)

gyro_scale_factor = 1 / 131.072  # بر اساس دیتا‌شیت MPU6050
accel_scale_factor = 1 / 2.0  # تقسیم بر ۲ برای شتاب سنج

while True:
    mpu_data = mpu.get_values()
    sensor_value1 = adc1.read()

    accel_x = mpu_data['AcX'] * accel_scale_factor
    accel_y = mpu_data['AcY'] * accel_scale_factor
    accel_z = mpu_data['AcZ'] * accel_scale_factor

    ax_degree = math.degrees(math.atan2(accel_x, accel_z))
    ax_text = "AX{:.0f}".format(ax_degree)

    ay_degree = math.degrees(math.atan2(accel_y, accel_z))
    ay_text = "AY{:.0f}".format(ay_degree)

    temperature = mpu_data['Tmp']

    t = "T{:.0f}".format(temperature)

    oled.text('o',60 - int(ay_degree), 28 - int(ax_degree))

    oled.text(t, 96, 0)
    oled.text(ax_text, 0, 0)
    oled.text(ay_text, 0, 10)

    oled.text(f"OUT:{sensor_value1}", 0,55)

    oled.show()

    time.sleep_ms(50)
    oled.fill(0)
