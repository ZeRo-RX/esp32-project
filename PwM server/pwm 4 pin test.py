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

# تنظیم پایه‌ها و PWM
pins = [Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]
pwms = [PWM(p, freq=5000) for p in pins]

# مقدار اولیه PWM برای هر پایه
for pwm in pwms:
    pwm.duty(512)

# تابعی برای کنترل PWM
def set_pwm(pin_index, duty):
    if 0 <= pin_index < len(pwms):
        pwms[pin_index].duty(duty)

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
        Set PWM for Pin 2: <input type="range" min="0" max="1023" name="pwm0" onchange="this.form.submit()" value="{pwm0}"><br>
        Set PWM for Pin 4: <input type="range" min="0" max="1023" name="pwm1" onchange="this.form.submit()" value="{pwm1}"><br>
        Set PWM for Pin 16: <input type="range" min="0" max="1023" name="pwm2" onchange="this.form.submit()" value="{pwm2}"><br>
        Set PWM for Pin 17: <input type="range" min="0" max="1023" name="pwm3" onchange="this.form.submit()" value="{pwm3}"><br>
    </form>
</body>
</html>
"""

while True:
    cl, addr = s.accept()
    #print('Client connected from', addr)
    request = cl.recv(1024)
    request = str(request)
    #print('Request:', request)

    # استخراج مقادیر PWM از درخواست
    pwm_values = [pwms[i].duty() for i in range(4)]  # مقدار پیش‌فرض برابر با مقدار فعلی
    for i in range(4):
        pwm_str = f'pwm{i}='
        start = request.find(pwm_str)
        if start != -1:
            try:
                pwm_value = int(request[start + len(pwm_str):].split(' ')[0].split('&')[0])
                if 0 <= pwm_value <= 1023:
                    pwm_values[i] = pwm_value
                    set_pwm(i, pwm_value)
            except ValueError:
                pass

    response = html.format(pwm0=pwm_values[0], pwm1=pwm_values[1], pwm2=pwm_values[2], pwm3=pwm_values[3])
    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n')
    cl.send('Connection: close\r\n')
    cl.send(f'Content-Length: {len(response)}\r\n')
    cl.send('\r\n')
    cl.sendall(response)
    cl.close()
