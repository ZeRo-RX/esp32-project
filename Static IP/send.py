import network
import time
import socket
import random

# SSID (نام شبکه) و رمز عبور شبکه WiFi خود را وارد کنید
WIFI_SSID = ""
WIFI_PASSWORD = ""

# آدرس IP و درگاه بک‌آپ را وارد کنید
DESTINATION_IP = "192.168.1.124"
DESTINATION_PORT = 80

# تنظیمات شبکه WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# انتظار برای اتصال به WiFi
while not wifi.isconnected():
    time.sleep(1)

print("متصل به WiFi")

# تنظیم آدرس IP برای ESP32
esp32_ip = "192.168.1.150"  # آدرس IP مورد نظر را وارد کنید
esp32_subnet_mask = "255.255.255.0"  # زیرشبکه مورد نظر را وارد کنید
esp32_gateway = "192.168.1.1"  # دروازه پیش فرض مورد نظر را وارد کنید

wifi.ifconfig((esp32_ip, esp32_subnet_mask, esp32_gateway, esp32_gateway))

print("آدرس IP برای ESP32 تنظیم شد:", wifi.ifconfig())

# برقراری ارتباط با مقصد
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((DESTINATION_IP, DESTINATION_PORT))

for i in 1000:# ارسال 4 عدد تصادفی به مقصد
    random_numbers = [str(random.randint(0, 100)) for _ in range(400)]
    data_to_send = ' '.join(random_numbers)
    sock.send(data_to_send.encode())

    print("داده ارسال شد به مقصد:", data_to_send)
    time.sleep(100)
# بستن اتصال
#sock.close()
#print("اتصال بسته شد")
