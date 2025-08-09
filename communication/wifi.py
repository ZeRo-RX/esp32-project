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

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("سرور آماده است و در حال گوش دادن به پورت ۸۰")

    while True:
        cl, addr = s.accept()
        print('اتصال جدید از', addr)

        request = cl.recv(1024)
        print("پیام دریافتی:")
        print(request)

        response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
                      <html><body><h1>پیام شما دریافت شد!</h1></body></html>"""
        cl.send(response)
        cl.close()

# مشخصات شبکه وای فای (Access Point)
SSID = 'ESP32_AP'
PASSWORD = '123456789'

# فراخوانی توابع
create_wifi_ap(SSID, PASSWORD)
start_server()
