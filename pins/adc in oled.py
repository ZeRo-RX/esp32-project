from machine import I2C , ADC , Pin
import time
import ssd1306

i2c = I2C(scl=Pin(22), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Set ADC pin to input
adc1 = ADC(14)
while True:
# Read the analog value from the sensor
    sensor_value1 = adc1.read()
# Print the sensor value to the console
    oled.fill(0)  # Clear the screen
    oled.text(f"OUT:{sensor_value1}", 0, 0)
    oled.show()

    time.sleep_ms(500)
