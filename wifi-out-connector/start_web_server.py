from webServer import WebServer


WIFI_SSID = ""
WIFI_PASSWORD = ""

pin_numbers = [2, 4, 16, 17, 5, 18, 19, 3]

web_server = WebServer(
    WIFI_SSID, WIFI_PASSWORD, pin_numbers
)  # Create an object of the WebServer class

try:
    web_server.start_server()  # Running a web server

except KeyboardInterrupt as err:
    pass
