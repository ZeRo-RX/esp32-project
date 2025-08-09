import network
import socket
import neopixel
import machine

# تنظیمات وای‌فای
SSID = ''
PASSWORD = ''

# راه‌اندازی وای‌فای
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, PASSWORD)

while not station.isconnected():
    pass

print('Connection successful')
print(station.ifconfig())

# تنظیمات نئوپیکسل
PIN = 2  # پینی که به نئوپیکسل وصل است
NUM_PIXELS = 8  # تعداد نئوپیکسل‌ها
np = neopixel.NeoPixel(machine.Pin(PIN), NUM_PIXELS)

# تابع برای تنظیم رنگ نئوپیکسل
def set_color(r, g, b):
    print(f"Setting color to R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)  # تغییر ترتیب به GRB
    np.write()

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

print('listening on', addr)

while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    if 'GET /?color=' in request:
        try:
            color = request.split('color=')[1].split(' ')[0]
            color = urldecode(color).lstrip('#')  # تفسیر کاراکترهای URL و حذف #
            r = int(color[0:2], 16)  # تبدیل به عدد صحیح
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            print(f"Received color R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
            set_color(r, g, b)
        except Exception as e:
            print('Error:', e)

    response = """<!DOCTYPE html>
    <html>
    <head>
        <title>RGB Control</title>
        <style>
            body { text-align: center; font-family: Arial; }
            #colorPicker { width: 300px; height: 300px; border: none; }
        </style>
    </head>
    <body>
        <h1>ESP32 RGB Control</h1>
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
    </html>
    """

    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n')
    cl.send('Connection: close\r\n\r\n')
    cl.sendall(response)
    cl.close()
