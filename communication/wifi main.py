import network
import socket

# ایجاد شبکه وای فای توسط ESP32
def create_wifi_ap(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)

    while not ap.active():
        pass

    print("شبکه وای فای ساخته شد!")
    print(ap.ifconfig())

# ایجاد سرور برای دریافت پیام‌ها
def start_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(1)

    print("سرور آماده است و در حال گوش دادن به پورت ۸۰")

    while True:
        cl, addr = s.accept()
        print('اتصال جدید از', addr)

        while True:
            request = cl.recv(1024)
            if not request:
                break
            print("پیام دریافتی:")
            print(request.decode())

        cl.close()

# مشخصات شبکه وای فای (Access Point)
SSID = 'ESP32_AP'
PASSWORD = ''

# فراخوانی توابع
create_wifi_ap(SSID, PASSWORD)
start_server()
