from webServer import WebServer
from GY521_SSD1306_i2c_move_and_show import SensorModule


WIFI_SSID = ""
WIFI_PASSWORD = ""

pin_numbers = [2, 4, 16, 17, 5, 18, 19, 3]
sensor_module = SensorModule() 

web_server = WebServer(WIFI_SSID, WIFI_PASSWORD, pin_numbers) # Create an object of the WebServer class 

#web_server.start_server()



web_server.start_server()







