import network
import socket
import machine
import ujson
import OLED

# تنظیمات I2C برای OLED
i2c = machine.SoftI2C(scl=machine.Pin(9), sda=machine.Pin(8))
oled = OLED.SSD1306_I2C(128, 64, i2c)

# اتصال به وای‌فای
ssid = ''
password = ''

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("در حال اتصال به وای‌فای...")
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print("اتصال برقرار شد:", wlan.ifconfig())
    return wlan.ifconfig()[0]

ip = connect_wifi()

# صفحه HTML برای ماتریس
html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>ESP32 OLED Drawing</title>
  <style>
    body {
      background-color: #0d0d0d;
      color: #ffffff;
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 20px;
    }

    h2 {
      margin-bottom: 20px;
      color: #00ffcc;
    }

    .canvas-container {
      border: 3px solid #00ffcc;
      padding: 10px;
      background-color: #000;
      box-shadow: 0 0 20px #00ffcc44;
    }

    canvas {
      image-rendering: pixelated;
      cursor: crosshair;
      background-color: black;
    }

    #note {
      margin-top: 15px;
      color: #888;
      font-size: 0.9em;
    }
  </style>
</head>
<body>
  <h2>ESP32 OLED Drawing Pad</h2>
  <div class="canvas-container">
    <canvas id="oled" width="640" height="320"></canvas>
  </div>
  <div id="note">ماتریس بزرگ‌نمایی شده - اندازه واقعی OLED: 128x64</div>

  <script>
    const scale = 5; // هر پیکسل OLED = 5x5 پیکسل در canvas
    const canvas = document.getElementById('oled');
    const ctx = canvas.getContext('2d');
    let drawing = false;

    // رسم یک پیکسل سفید در مختصات OLED
    function drawPixel(x, y) {
      ctx.fillStyle = "white";
      ctx.fillRect(x * scale, y * scale, scale, scale);
      fetch("/pixel", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({x: x, y: y})
      });
    }

    function getXY(e) {
      const rect = canvas.getBoundingClientRect();
      const x = Math.floor((e.clientX - rect.left) / scale);
      const y = Math.floor((e.clientY - rect.top) / scale);
      return {x, y};
    }

    canvas.addEventListener('mousedown', (e) => {
      drawing = true;
      const {x, y} = getXY(e);
      drawPixel(x, y);
    });

    canvas.addEventListener('mousemove', (e) => {
      if (!drawing) return;
      const {x, y} = getXY(e);
      drawPixel(x, y);
    });

    canvas.addEventListener('mouseup', () => drawing = false);
    canvas.addEventListener('mouseleave', () => drawing = false);
  </script>
</body>
</html>
"""



# تابع هندل کردن درخواست‌ها
def serve():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(5)
    print("در حال اجرا در http://%s/" % ip)

    while True:
        cl, addr = s.accept()
        print('اتصال جدید:', addr)
        req = cl.recv(1024)
        req_str = req.decode('utf-8')

        if "GET / " in req_str or "GET /HTTP" in req_str:
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
            cl.sendall(html)
        elif "POST /pixel" in req_str:
            # دریافت مختصات
            body = req_str.split('\r\n\r\n')[1]
            data = ujson.loads(body)
            x, y = int(data['x']), int(data['y'])

            # نمایش در OLED
            oled.pixel(x, y, 1)
            oled.show()

            cl.send('HTTP/1.0 200 OK\r\n\r\n')
            cl.send("OK")
        else:
            cl.send('HTTP/1.0 404 Not Found\r\n\r\n')

        cl.close()

# شروع سرور
serve()
