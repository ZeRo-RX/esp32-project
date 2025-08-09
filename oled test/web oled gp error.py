import network
import socket
import machine
import ujson
import OLED

# تنظیمات I2C برای OLED
i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21))
oled = OLED.SSD1306_I2C(128, 64, i2c)

# اتصال به وای‌فای
ssid = 'ZeRo2'
password = 'karimi1397'

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
      margin-top: 10px;
      color: #888;
      font-size: 0.9em;
    }

    .btns {
      margin-top: 15px;
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      justify-content: center;
    }

    button {
      padding: 6px 12px;
      background-color: #00ffcc;
      border: none;
      border-radius: 5px;
      color: black;
      font-weight: bold;
      cursor: pointer;
    }

    input[type="file"] {
      margin-top: 10px;
      color: #ccc;
    }
  </style>
</head>
<body>
  <h2>ESP32 OLED Drawing Pad</h2>
  <div class="canvas-container">
    <canvas id="oled" width="640" height="320"></canvas>
  </div>

  <div class="btns">
    <button onclick="clearDisplay()">پاک کردن نمایشگر</button>
    <button onclick="sendToESP()">نمایش روی OLED</button>
  </div>

  <input type="file" id="imgUpload" accept="image/*">
  <div id="note">تصویر یا نقاشی شما روی canvas کشیده می‌شود و با یک کلیک به OLED ارسال خواهد شد</div>

  <script>
    const scale = 5;
    const canvas = document.getElementById('oled');
    const ctx = canvas.getContext('2d');
    let drawing = false;

    // ماتریس دودویی تصویر
    let pixelMatrix = Array.from({length: 64}, () => Array(128).fill(0));

    function drawPixel(x, y) {
      ctx.fillStyle = "white";
      ctx.fillRect(x * scale, y * scale, scale, scale);
      pixelMatrix[y][x] = 1;
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

    function clearDisplay() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pixelMatrix = Array.from({length: 64}, () => Array(128).fill(0));
      fetch("/clear");
    }

    function sendToESP() {
      fetch("/bitmap", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({data: pixelMatrix})
      }).then(() => {
        console.log("ارسال کامل شد.");
      });
    }

    // آپلود عکس و تبدیل به سیاه‌سفید
    document.getElementById("imgUpload").addEventListener("change", function(e) {
      const file = e.target.files[0];
      const reader = new FileReader();

      reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
          const offCanvas = document.createElement("canvas");
          offCanvas.width = 128;
          offCanvas.height = 64;
          const offCtx = offCanvas.getContext("2d");
          offCtx.drawImage(img, 0, 0, 128, 64);

          ctx.clearRect(0, 0, canvas.width, canvas.height);
          pixelMatrix = Array.from({length: 64}, () => Array(128).fill(0));

          for (let y = 0; y < 64; y++) {
            for (let x = 0; x < 128; x++) {
              const pixel = offCtx.getImageData(x, y, 1, 1).data;
              const avg = (pixel[0] + pixel[1] + pixel[2]) / 3;
              if (avg < 128) {
                drawPixel(x, y);
              }
            }
          }
        };
        img.src = event.target.result;
      };
      reader.readAsDataURL(file);
    });
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
        print("اتصال جدید:", addr)

        def recv_all(sock):
            data = b''
            while True:
                part = sock.recv(1024)
                data += part
                if len(part) < 1024:
                    break
            return data

        req = recv_all(cl)
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


            cl.send('HTTP/1.0 200 OK\r\n\r\n')
            cl.send("OK")
            
        elif "POST /bitmap" in req_str:
            try:
                body = req_str.split('\r\n\r\n', 1)[1]
                data = ujson.loads(body)
                bitmap = data["data"]
                print("Bitmap received")
                for y in range(64):
                    for x in range(128):
                        oled.pixel(x, y, int(bitmap[y][x]))
                oled.show()
                cl.send('HTTP/1.0 200 OK\r\n\r\n')
                cl.send("DONE")
            except Exception as e:
                cl.send('HTTP/1.0 400 Bad Request\r\n\r\n')
                cl.send("Error: " + str(e))
                print("خطای JSON:", e)                
        elif "GET /clear" in req_str:
            oled.fill(0)
            oled.show()
            cl.send('HTTP/1.0 200 OK\r\n\r\n')
            cl.send("CLEARED")

        else:
            cl.send('HTTP/1.0 404 Not Found\r\n\r\n')
        

        oled.show()
        cl.close()

# شروع سرور
serve()


