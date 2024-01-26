import time
import network
import socket
from machine import Pin

# نام و رمز عبور شبکه وای فای خود را وارد کنید
ssid = "ZeRo"
password = "karimi1397"

# ماژول وای فای را راه اندازی کنید
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# ماژول وای فای را به شبکه وصل کنید
wlan.connect(ssid, password)

# تا زمانی که ماژول به شبکه وصل نشود صبر کنید
while not wlan.isconnected():
    pass

# تعریف پین D2 به عنوان خروجی
pin2 = Pin(2, Pin.OUT)
# ایجاد سرویس وب ساده
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 80))
server.listen(1)

# تعریف تابع render()
def render(pin_state):
    # محتوای HTML را برای سرویس وب بازگردانید
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <title>xxx</title>
    </head>
    <body>
        <h1>po2:</h1>
        <p id="state">{pin_state}</p>
        <button onclick="turnOn()">on</button>
        <button onclick="turnOff()">off</button>
        <script>
            function turnOn() {{
                document.getElementById("state").innerHTML = "on";
                fetch("/on");
            }}

            function turnOff() {{
                document.getElementById("state").innerHTML = "off";
                fetch("/off");
            }}
        </script>
    </body>
    </html>
    """

# مقدار اولیه وضعیت پورت 2
state = "off"

while True:
    # پذیرفتن اتصال جدید
    connection, address = server.accept()

    # دریافت درخواست از مشتری
    request = connection.recv(1024)

    # پردازش درخواست
    if "GET /on HTTP/1.1" in request:
        # روشن کردن وب پورت 2
        state = "on"
        pin2.on()

    elif "GET /off HTTP/1.1" in request:
        # خاموش کردن وب پورت 2
        state = "off"
        pin2.off()

    # ارسال پاسخ به مشتری
    response = render(state)
    connection.send(response.encode())

    # بستن اتصال
    connection.close()

