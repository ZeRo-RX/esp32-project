import network
import socket
import time

# اتصال به شبکه وای‌فای ESP32 که به عنوان Access Point عمل می‌کند
def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        pass

    print("اتصال به شبکه برقرار شد!")
    print(wlan.ifconfig())

# ارسال داده به سرور
def send_data_to_server(host, port):
    addr = socket.getaddrinfo(host, port)[0][-1]

    s = socket.socket()
    s.connect(addr)

    counter = 0
    while True:
        message = f"عدد: {counter}"
        print(f"در حال ارسال: {message}")

        s.send(message.encode())
        counter += 1

        time.sleep(1)

    s.close()

# اطلاعات شبکه وای‌فای (SSID و رمز عبور)
SSID = 'ESP32_AP'
PASSWORD = ''

# اطلاعات سرور (آدرس IP و پورت)
HOST = '192.168.4.1'  # آدرس IP پیش‌فرض ESP32 به عنوان Access Point
PORT = 80

# فراخوانی توابع
connect_to_wifi(SSID, PASSWORD)
send_data_to_server(HOST, PORT)
