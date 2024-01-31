from machine import I2C, Pin
import mpu6050
import OLED
import time

i2c = I2C(scl=Pin(22), sda=Pin(21))
mpu = mpu6050.accel(i2c)
oled = OLED.SSD1306_I2C(128, 64, i2c)

while True:
    mpu_data = mpu.get_values()

    gyro_x = mpu_data['GyX']
    gyro_y = mpu_data['GyY']
    gyro_z = mpu_data['GyZ']

    accel_x = mpu_data['AcX']
    accel_y = mpu_data['AcY']
    accel_z = mpu_data['AcZ']

    temperature = mpu_data['Tmp']

    gx = "GX{}".format(gyro_x)
    gy = "GY{}".format(gyro_y)
    gz = "GZ{}".format(gyro_z)

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
