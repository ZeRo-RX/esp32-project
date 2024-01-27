from wifi_connector import WifiConnector
import machine
import socket
from html_generator import HtmlGenerator
import network
from pin_handler import PinHandler

class WebServer:
    def __init__(self, WIFI_SSID, WIFI_PASSWORD, pin_numbers):
        self.WIFI_SSID = WIFI_SSID
        self.WIFI_PASSWORD = WIFI_PASSWORD
        self.pin_numbers = pin_numbers
        self.pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]
        self.htmlGenerator = HtmlGenerator(pin_numbers)
        self.html = self.htmlGenerator.create_html()
        self.wifi_connector = WifiConnector(WIFI_SSID, WIFI_PASSWORD)
        self.pin_handler = PinHandler(self.pins, self.pin_numbers)

    def start_server(self):
        self.wifi_connector.connect()

        addr = network.WLAN().ifconfig()[0]
        print("Web server started on", addr)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((addr, 80))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            print("Client connected from", addr)

            request = conn.recv(1024)
            request = str(request)

            self.pin_handler.handle_request(request)

            conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

            # Sending the body of the message at once
            conn.sendall(self.html)
            conn.close()
