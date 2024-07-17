import network
import time
import socket

# SSID (نام شبکه) و رمز عبور شبکه WiFi خود را وارد کنید
WIFI_SSID = ""
WIFI_PASSWORD = ""

# آدرس IP و درگاه بک‌آپ را وارد کنید
BACKUP_IP = "192.168.1.1"
BACKUP_PORT = 80


# تنظیمات شبکه WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# انتظار برای اتصال به WiFi
while not wifi.isconnected():
    time.sleep(1)

print("Connected to WiFi")

# تنظیم آدرس IP برای ESP32
esp32_ip = "192.168.1.8"  # آدرس IP مورد نظر را وارد کنید
esp32_subnet_mask = "255.255.255.0"  # زیرشبکه مورد نظر را وارد کنید
esp32_gateway = "192.168.1.1"  # دروازه پیش فرض مورد نظر را وارد کنید

wifi.ifconfig((esp32_ip, esp32_subnet_mask, esp32_gateway, esp32_gateway))

print("IP address set for ESP32:", wifi.ifconfig())

# برقراری ارتباط با بک‌آپ
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((BACKUP_IP, BACKUP_PORT))
