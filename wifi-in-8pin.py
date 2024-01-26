import network
import machine
import socket
from html_generator import HtmlGenerator

WIFI_SSID = "ESP32_AP"  # نام شبکه
WIFI_PASSWORD = ""  # رمز عبور

pin_numbers = [2, 4, 16, 17, 5, 18, 19, 21]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]

htmlGenerator = HtmlGenerator(pin_numbers)
html = htmlGenerator.create_html()

def create_wifi_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=WIFI_SSID, password=WIFI_PASSWORD)
    print("WiFi Access Point created:", WIFI_SSID)


def handle_request(request):

    for i in range(len(pin_numbers)):
        if f"/pin{pin_numbers[i]}/on" in request:
            pins[i].on()
        elif f"/pin{pin_numbers[i]}/off" in request:
            pins[i].off()

    if "/allpin/on" in request:
        for i in range(len(pin_numbers)):
            pins[i].on()

    elif "/allpin/off" in request:
        for i in range(len(pin_numbers)):
            pins[i].off()



def start_web_server():
    create_wifi_ap()

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

        handle_request(request)

        # ارسال هدر به جای متن
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

        # ارسال بدنه پیام به صورت یکباره
        conn.sendall(html)
        conn.close()

start_web_server()
