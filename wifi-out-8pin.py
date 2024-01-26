import network
import machine
import socket
from html_generator import HtmlGenerator

WIFI_SSID = "SSID"
WIFI_PASSWORD = "PASSWORD"


pin_numbers = [2, 4, 16, 17, 5, 18, 19, 21]
pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]


htmlGenerator = HtmlGenerator(pin_numbers)
html = htmlGenerator.create_html()

def connect_to_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)
    while not wlan.isconnected():
        pass
    print("Connected to WiFi")


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
    connect_to_wifi()

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

        handle_request(request)


        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

        # ارسال بدنه پیام به صورت یکباره
        conn.sendall(html)
        conn.close()


start_web_server()
