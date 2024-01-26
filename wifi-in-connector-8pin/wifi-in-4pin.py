import network
import machine
import socket
from html_generator import HtmlGenerator
from pin_handler import PinHandler
from wifi_ap_module import WifiAPManager

WIFI_SSID = "ESP32_AP"  # نام شبکه
WIFI_PASSWORD = ""  # رمز عبور

pin_numbers = [2, 4, 18, 19]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]

htmlGenerator = HtmlGenerator(pin_numbers)
html = htmlGenerator.create_html()

pin_handler = PinHandler(pins, pin_numbers)

wifi_manager = WifiAPManager(WIFI_SSID, WIFI_PASSWORD)

def start_web_server():
    wifi_manager.create_wifi_ap()

    addr = "192.168.4.1"  # آدرس IP شبکه ایجاد شده توسط ESP32
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

        # ارسال هدر به جای متن
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

        # ارسال بدنه پیام به صورت یکباره
        conn.sendall(html)
        conn.close()

start_web_server()