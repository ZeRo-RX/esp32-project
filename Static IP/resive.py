import network
import time
import socket

# SSID (نام شبکه) و رمز عبور شبکه WiFi خود را وارد کنید
WIFI_SSID = "ZeRo"
WIFI_PASSWORD = "karimi1397"

# آدرس IP و درگاه بک‌آپ را وارد کنید
DESTINATION_IP = "192.168.1.1"
DESTINATION_PORT = 80

# تنظیمات شبکه WiFi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# انتظار برای اتصال به WiFi
#while not wifi.isconnected():
 #   time.sleep(1)

print("متصل به WiFi")

# تنظیم آدرس IP برای ESP32
esp32_ip = "192.168.1.124"  # آدرس IP مورد نظر را وارد کنید
esp32_subnet_mask = "255.255.255.0"  # زیرشبکه مورد نظر را وارد کنید
esp32_gateway = "192.168.1.1"  # دروازه پیش فرض مورد نظر را وارد کنید

wifi.ifconfig((esp32_ip, esp32_subnet_mask, esp32_gateway, esp32_gateway))

print("آدرس IP برای ESP32 تنظیم شد:", wifi.ifconfig())

# برقراری اتصال به مقصد
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('0.0.0.0', DESTINATION_PORT))
sock.listen(1)

print("در حال گوش دادن برای اتصال...")

while True:
    try:
        conn, addr = sock.accept()
        print('اتصال برقرار شد به:', addr)

        # دریافت و چاپ داده‌های دریافتی
        data_received = conn.recv(1024).decode()
        print("داده دریافت شده:", data_received)
    except Exception as e:
        print("خطا:", e)
    finally:
        # بستن اتصال
        conn.close()
        print("اتصال بسته شد")
