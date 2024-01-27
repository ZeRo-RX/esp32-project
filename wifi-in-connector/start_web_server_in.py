from web_server import WebServer
from utils.logging import Logger

logger = Logger()

WIFI_SSID = "ESP32_AP"  # WIFI_SSID
WIFI_PASSWORD = ""  #  WIFI_PASSWORD

pin_numbers = [2, 4, 16, 17, 5, 18, 19, 21]

web_server = WebServer(WIFI_SSID, WIFI_PASSWORD, pin_numbers) # Create an object of the WebServer class

try:
    web_server.start_server() # Running a web server

except KeyboardInterrupt as err:
    pass
