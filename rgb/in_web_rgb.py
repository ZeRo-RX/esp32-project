import network
import socket
import neopixel
import machine
from time import sleep
import _thread  # برای اجرای تابع rainbow در یک thread جداگانه

PIN2 = 2  # پین متصل به نئوپیکسل
NUM_PIXELS = 8  # تعداد نئوپیکسل‌ها
np2 = neopixel.NeoPixel(machine.Pin(PIN2), NUM_PIXELS)


colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255), (0, 57, 75)]

for color in colors:
    for i in range(8):
        np2[i] = color
        np2.write()
        sleep(0.1)
    sleep(0.1)


rainbowList = [(126, 0, 0), (123, 3, 0), (120, 6, 0), (117, 9, 0), (114, 12, 0), (111, 15, 0), (108, 18, 0), (105, 21, 0), (102, 24, 0), (99, 27, 0), (96, 30, 0), (93, 33, 0), (90, 36, 0), (87, 39, 0), (84, 42, 0),
(81, 45, 0), (78, 48, 0), (75, 51, 0), (72, 54, 0), (69, 57, 0), (66, 60, 0), (63, 63, 0), (60, 66, 0), (57, 69, 0), (54, 72, 0), (51, 75, 0), (48, 78, 0), (45, 81, 0), (42, 84, 0), (39, 87, 0),
(36, 90, 0), (33, 93, 0), (30, 96, 0), (27, 99, 0), (24, 102, 0), (21, 105, 0), (18, 108, 0), (15, 111, 0), (12, 114, 0), (9, 117, 0), (6, 120, 0), (0, 126, 0), (0, 123, 3), (0, 120, 6), (0, 117, 9),
(0, 114, 12), (0, 111, 15), (0, 108, 18), (0, 105, 21), (0, 102, 24), (0, 99, 27), (0, 96, 30), (0, 93, 33), (0, 90, 36), (0, 87, 39), (0, 84, 42), (0, 81, 45), (0, 78, 48), (0, 75, 51), (0, 72, 54),
(0, 69, 57), (0, 66, 60), (0, 63, 63), (0, 60, 66), (0, 57, 69), (0, 54, 72), (0, 51, 75), (0, 48, 78), (0, 45, 81), (0, 42, 84), (0, 39, 87), (0, 36, 90), (0, 33, 93), (0, 30, 96), (0, 27, 99),
(0, 24, 102), (0, 21, 105), (0, 18, 108), (0, 15, 111), (0, 12, 114), (0, 9, 117), (0, 6, 120), (0, 3, 123), (0, 0, 126), (3, 0, 123), (6, 0, 120), (9, 0, 117), (12, 0, 114), (15, 0, 111), (18, 0, 108),
(21, 0, 105), (24, 0, 102), (27, 0, 99), (30, 0, 96), (33, 0, 93), (36, 0, 90), (39, 0, 87), (42, 0, 84), (45, 0, 81), (48, 0, 78), (51, 0, 75), (54, 0, 72), (57, 0, 69), (60, 0, 66), (63, 0, 63),
(66, 0, 60), (69, 0, 57), (72, 0, 54), (75, 0, 51), (78, 0, 48), (81, 0, 45), (84, 0, 42), (87, 0, 39), (90, 0, 36), (93, 0, 33), (96, 0, 30), (99, 0, 27), (102, 0, 24), (105, 0, 21), (108, 0, 18),
(111, 0, 15), (114, 0, 12), (117, 0, 9), (120, 0, 6), (123, 0, 3)]
# تنظیمات نقطه دسترسی
SSID = ""
PASSWORD = ""

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=SSID, password=PASSWORD, authmode=network.AUTH_WPA2_PSK)

print("نقطه دسترسی ایجاد شد")
print("آدرس IP:", ap.ifconfig()[0])

# متغیر وضعیت برای کنترل اجرای افکت رنگین‌کمانی
rainbow_running = False

# تابع برای تنظیم رنگ نئوپیکسل‌ها
def set_color(r, g, b):
    global rainbow_running
    rainbow_running = False  # متوقف کردن افکت رنگین‌کمانی
    print(f"تنظیم رنگ به R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
    for i in range(NUM_PIXELS):
        np2[i] = (r, g, b)
    np2.write()

# تابع برای تفسیر URL-encoded
def urldecode(url):
    res = ""
    i = 0
    while i < len(url):
        if url[i] == "%":
            res += chr(int(url[i + 1 : i + 3], 16))
            i += 3
        else:
            res += url[i]
            i += 1
    return res

# تابع برای اجرای افکت رنگین‌کمانی
def rainbow():
    global rainbow_running
    rainbow_running = True
    while rainbow_running:
        rainbowList.append(rainbowList.pop(0)) # چرخش لیست رنگ‌ها
        for i in range(NUM_PIXELS):
            np2[i] = rainbowList[i]
        np2.write()
        sleep(0.08)
    print("افکت رنگین‌کمانی متوقف شد.")

# ساختن وب سرور
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print("در حال گوش دادن در", addr)

while True:
    cl, addr = s.accept()
    print("ارتباط از طرف مشتری", addr)
    request = cl.recv(1024)
    request = str(request)
    print("محتوا = %s" % request)

    if "GET /?action=rainbow" in request:
        if not rainbow_running:  # اگر افکت رنگین‌کمانی در حال اجرا نباشد
            _thread.start_new_thread(rainbow, ())  # اجرای افکت در یک thread جداگانه
    elif "GET /?color=" in request:
        try:
            color = request.split("color=")[1].split(" ")[0]
            color = urldecode(color).lstrip("#")  # تفسیر کاراکترهای URL و حذف #
            r = int(color[0:2], 16)  # تبدیل به عدد صحیح
            g = int(color[2:4], 16)
            b = int(color[4:6], 16)
            print(f"دریافت رنگ R: {r}, G: {g}, B: {b}")  # پیام چاپ برای رفع اشکال
            set_color(r, g, b)  # تنظیم رنگ جدید و توقف افکت رنگین‌کمانی
        except Exception as e:
            print("خطا:", e)

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
            margin-top: 50px;
            direction: rtl;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            height: 100vh;
        }
        h1 {
            color: #fff;
        }
        #colorPicker, #rainbowButton {
            width: 100px;
            height: 100px;
            border: groove;
            cursor: pointer;
            border-radius: 3%;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 10px;
        }
        #colorPicker {
            background: linear-gradient(135deg, #ffafbd, #ffc3a0, #ffafbd);
        }
        #colorPicker:hover {
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
            background: linear-gradient(135deg, #ffc3a0, #ffafbd, #ffc3a0);
        }
        #rainbowButton {
            background: linear-gradient(45deg, red, orange, yellow, green, blue, indigo, violet);
            border: none;
            box-shadow: 0 0 15px rgba(0, 0, 0, 0.4);
            transition: all 0.4s ease;
            background-size: 300% 300%;
            animation: rainbowAnimation 4s infinite alternate;
            color: white;
        }

        #rainbowButton:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255, 255, 255, 0.8);
        }

        @keyframes rainbowAnimation {
            0% { background-position: 0% 50%; }
            100% { background-position: 100% 50%; }
        }
    </style>
</head>
<body>
    <h1>RGB control with ESP32</h1>
    <input type="color" id="colorPicker">
    <br>
    <button id="rainbowButton">R</button>
    <script>
        document.getElementById('colorPicker').addEventListener('change', function() {
            var color = this.value;
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/?color=' + encodeURIComponent(color), true);
            xhr.send();
        });

        document.getElementById('rainbowButton').addEventListener('click', function() {
            var xhr = new XMLHttpRequest();
            xhr.open('GET', '/?action=rainbow', true);
            xhr.send();
        });
    </script>
</body>
</html>

        """

    cl.send("HTTP/1.1 200 OK\r\n")
    cl.send("Content-Type: text/html\r\n")
    cl.send("Connection: close\r\n\r\n")
    cl.sendall(response)
    cl.close()
