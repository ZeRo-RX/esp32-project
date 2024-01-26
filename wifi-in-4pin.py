import network
from machine import Pin as Pins
import socket

WIFI_SSID = "ESP32_AP"  # نام شبکه
WIFI_PASSWORD = ""  # رمز عبور

pt = Pins.OUT

PIN2 = Pins(2, pt)
PIN4 = Pins(4, pt)
PIN18 = Pins(18, pt)
PIN19 = Pins(19, pt)


def create_wifi_ap():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=WIFI_SSID, password=WIFI_PASSWORD)
    print("WiFi Access Point created:", WIFI_SSID)


def handle_request(request):
    if "/pin2/on" in request:
        PIN2.on()
    elif "/pin2/off" in request:
        PIN2.off()

    if "/pin4/on" in request:
        PIN4.on()
    elif "/pin4/off" in request:
        PIN4.off()

    if "/pin18/on" in request:
        PIN18.on()
    elif "/pin18/off" in request:
        PIN18.off()

    if "/pin19/on" in request:
        PIN19.on()
    elif "/pin19/off" in request:
        PIN19.off()

    if "/allpin/on" in request:
        PIN2.on()
        PIN4.on()
        PIN18.on()
        PIN19.on()
    elif "/allpin/off" in request:
        PIN2.off()
        PIN4.off()
        PIN18.off()
        PIN19.off()


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

        html = """<!DOCTYPE html>
                <html>
                <head>
                    <title>ESP32 Web Server</title>
                    <style>
                        .button {
                            background-color: #4CAF50;
                            border: none;
                            color: white;
                            padding: 16px 32px;
                            text-align: center;
                            text-decoration: none;
                            display: inline-block;
                            font-size: 16px;
                            margin: 4px 2px;
                            cursor: pointer;
                            border-radius: 8px;
                        }
                    </style>
                </head>
                <body>
                    <h1>ESP32 Web Server</h1>
                    <button class="button" onclick="window.location.href='/pin2/on'"> On Pin 2</button>
                    <button class="button" onclick="window.location.href='/pin2/off'"> Off Pin 2</button>
                    <button class="button" onclick="window.location.href='/pin4/on'"> On Pin 4</button>
                    <button class="button" onclick="window.location.href='/pin4/off'"> Off Pin 4</button>
                    <h1>ESP32 Web Server</h1>
                    <button class="button" onclick="window.location.href='/pin18/on'"> On Pin 18</button>
                    <button class="button" onclick="window.location.href='/pin18/off'"> Off Pin 18</button>
                    <button class="button" onclick="window.location.href='/pin19/on'"> On Pin 19</button>
                    <button class="button" onclick="window.location.href='/pin19/off'"> Off Pin 19</button>
                    <h1>ESP32 Web Server</h1>
                    <button class="button" onclick="window.location.href='/allpin/on'"> On all pin</button>
                    <button class="button" onclick="window.location.href='/allpin/off'"> Off all pin</button>
                    <button class="button" onclick="window.location.href='/xx/on'"> On xx pin</button>
                    <button class="button" onclick="window.location.href='/xx/off'"> Off xx pin</button>



                </body>


                </html>"""

        # ارسال هدر به جای متن
        conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")

        # ارسال بدنه پیام به صورت یکباره
        conn.sendall(html)
        conn.close()


start_web_server()
