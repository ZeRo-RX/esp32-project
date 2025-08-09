import network
import time

def connect_to_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # تنظیمات IP ثابت
    wlan.ifconfig(('192.168.4.2', '255.255.255.0', '192.168.4.1', '192.168.4.1'))

    wlan.connect(ssid, password)

    max_wait = 20
    while max_wait > 0:
        if wlan.isconnected():
            print("اتصال به شبکه برقرار شد!")
            print(wlan.ifconfig())
            break
        else:
            print(f"در حال اتصال به شبکه وای‌فای... (تاخیر {20 - max_wait + 1})")
            time.sleep(1)
            max_wait -= 1

    if not wlan.isconnected():
        print("اتصال به شبکه وای‌فای با مشکل مواجه شد")

SSID = 'ESP32_AP'
PASSWORD = ''

connect_to_wifi(SSID, PASSWORD)
