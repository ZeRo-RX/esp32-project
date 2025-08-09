import network
import socket
import neopixel
import machine
from time import sleep

PIN2 = 2  # پین متصل به نئوپیکسل
PIN4 = 4
NUM_PIXELS = 8  # تعداد نئوپیکسل‌ها
np2 = neopixel.NeoPixel(machine.Pin(PIN2), NUM_PIXELS)
np4 = neopixel.NeoPixel(machine.Pin(PIN4), NUM_PIXELS)

for i in range(8):
    np2[i] = (255,0,0)
    np4[i] = (255,0,0)
    np2.write()
    np4.write()
    sleep(0.1)

for i in range(8):
    np2[i] = (0,255,0)
    np4[i] = (0,255,0)
    np2.write()
    np4.write()
    sleep(0.1)

for i in range(8):
    np2[i] = (0,0,255)
    np4[i] = (0,0,255)
    np2.write()
    np4.write()
    sleep(0.1)

for i in range(8):
    np2[i] = (255,255,255)
    np4[i] = (255,255,255)
    np2.write()
    np4.write()
    sleep(0.1)

for i in range(8):
    np2[i] = (0,57,75)
    np4[i] = (0,57,75)
    np2.write()
    np4.write()
    sleep(0.1)
# تنظیمات وای‌فای
SSID = ''
PASSWORD = ''

# راه‌اندازی
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

# صبر تا اتصال وای‌فای برقرار شود
while not station.isconnected():
    pass

print('اتصال موفق')
print(station.ifconfig())

# تنظیمات نئوپیکسل# تابع برای تنظیم رنگ نئوپیکسل‌ها
def set_color(r, g, b):
    print(f"تنظیم رنگ به R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
    for i in range(NUM_PIXELS):
        np2[i] = (r, g, b)
        np4[i] = (r, g, b)  # تغییر ترتیب به GRB
    np2.write()
    np4.write()
# تابع برای تفسیر URL-encoded
def urldecode(url):
    res = ''
    i = 0
    while i < len(url):
        if url[i] == '%':
            res += chr(int(url[i+1:i+3], 16))
            i += 3
        else:
            res += url[i]
            i += 1
    return res

# ساختن وب سرور
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('در حال گوش دادن در', addr)

while True:
    cl, addr = s.accept()
    print('ارتباط از طرف مشتری', addr)
    request = cl.recv(1024)
    request = str(request)
    print('محتوا = %s' % request)

    if 'GET /?color=' in request:
        try:
            color = request.split('color=')[1].split(' ')[0]
            color = urldecode(color).lstrip('#')  # تفسیر کاراکترهای URL و حذف #
            r = int(color[0:2], 16)  # تبدیل به عدد صحیح
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            print(f"دریافت رنگ R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
            set_color(r, g, b)
        except Exception as e:
            print('خطا:', e)

    response = """<!DOCTYPE html>
<html lang="fa">
<head>
    <meta charset="UTF-8">
    <title>RGB control</title>
    <style>
        body {
            text-align: center;
            font-family: Arial, sans-serif;
            background-color: #333;
            margin-top: 100px;
            direction: rtl;
        }
        h1 {
            color: #fff;
        }
        #colorPicker {
            width: 100px;
            height: 100px;
            border: groove;
            cursor: pointer;
            border-radius: 3%;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            transition: box-shadow 0.3s ease, background 0.3s ease;
            background: linear-gradient(135deg, #ffafbd, #ffc3a0, #ffafbd);

        }
        #colorPicker:hover {
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.6);
            background: linear-gradient(135deg, #ffc3a0, #ffafbd, #ffc3a0);
        }
    </style>
</head>
<body>
    <h1>RGB control with ESP32</h1>
    <input type="color" id="colorPicker">
    <script>
        document.getElementById('colorPicker').addEventListener('change', function() {
            var color = this.value;
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/?color=' + encodeURIComponent(color), true);
            xhr.send();
        });
    </script>
</body>

        """

    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n')
    cl.send('Connection: close\r\n\r\n')
    cl.sendall(response)
    cl.close()

