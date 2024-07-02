import network

def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print('Connection successful')
    print(station.ifconfig())

# پارامترهای وای‌فای خود را اینجا وارد کنید
ssid = 'ZeRo2'
password = 'karimi1397'
connect_to_wifi(ssid, password)

import socket
from machine import Pin, PWM

# تنظیم پایه و PWM
led = Pin(2, Pin.OUT)
pwm = PWM(led, freq=5000)
pwm.duty(512)  # مقدار اولیه PWM

# تابعی برای کنترل PWM
def set_pwm(duty):
    pwm.duty(duty)

# ایجاد سرور و گوش دادن به درخواست‌ها
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

html = """<!DOCTYPE html>
<html>
<head>
    <title>ESP32 PWM Control</title>
</head>
<body>
    <h1>ESP32 PWM Control</h1>
    <form action="/" method="get">
        Set PWM: <input type="range" min="0" max="1023" name="pwm" onchange="this.form.submit()" value="{pwm}">
    </form>
</body>
</html>
"""

while True:
    cl, addr = s.accept()
    print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    print('Request:', request)

    # استخراج مقدار PWM از درخواست
    pwm_value = 512  # مقدار پیش‌فرض
    if '/?pwm=' in request:
        try:
            pwm_value = int(request.split('/?pwm=')[1].split(' ')[0])
            if 0 <= pwm_value <= 1023:
                set_pwm(pwm_value)
        except ValueError:
            pass

    response = html.format(pwm=pwm_value)
    cl.send('HTTP/1.1 200 OK\n')
    cl.send('Content-Type: text/html\n')
    cl.send('Connection: close\n\n')
    cl.sendall(response)
    cl.close()
