from machine import I2C, Pin
import mpu6050
import OLED
import time
import math

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu = mpu6050.accel(i2c)
oled = OLED.SSD1306_I2C(128, 64, i2c)

gyro_scale_factor = 1 / 131.072  # بر اساس دیتا‌شیت MPU6050
accel_scale_factor = 1 / 2.0  # تقسیم بر ۲ برای شتاب سنج

while True:
    mpu_data = mpu.get_values()

    gyro_x = mpu_data['GyX'] * gyro_scale_factor
    gyro_y = mpu_data['GyY'] * gyro_scale_factor
    gyro_z = mpu_data['GyZ'] * gyro_scale_factor

    accel_x = mpu_data['AcX'] * accel_scale_factor
    accel_y = mpu_data['AcY'] * accel_scale_factor
    accel_z = mpu_data['AcZ'] * accel_scale_factor

    temperature = mpu_data['Tmp']

    gx = "GX{:.2f}".format(gyro_x)
    gy = "GY{:.2f}".format(gyro_y)
    gz = "GZ{:.2f}".format(gyro_z)

    ax = "AX{}".format(accel_x)
    ay = "AY{}".format(accel_y)
    az = "AZ{}".format(accel_z)

    t = "T{}".format(temperature)

    oled.text(gx, 0, 0)
    oled.text(gy, 0, 10)
    oled.text(gz, 0, 20)

    oled.text(ax, 0, 30)
    oled.text(ay, 0, 40)
    oled.text(az, 0, 50)

    oled.text(t, 64, 20)

    oled.show()

    time.sleep(0.5)
    oled.fill(0)
