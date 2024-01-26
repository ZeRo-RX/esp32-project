from wifi_connector import WifiConnector
import machine
import socket
from html_generator import HtmlGenerator
import network
from pin_handler import PinHandler

WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"

pin_numbers = [2, 4, 16, 17, 5, 18, 19, 21]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]

htmlGenerator = HtmlGenerator(pin_numbers)
html = htmlGenerator.create_html()

wifi_connector = WifiConnector(WIFI_SSID, WIFI_PASSWORD)

pin_handler = PinHandler(pins, pin_numbers)


def start_web_server():
    wifi_connector.connect()

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

        pin_handler.handle_request(request)

        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

        # ارسال بدنه پیام به صورت یکباره
        conn.sendall(html)
        conn.close()

start_web_server()
