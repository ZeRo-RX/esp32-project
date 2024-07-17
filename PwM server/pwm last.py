import network
import socket
from machine import Pin, PWM

# تابع برای اتصال به WiFi
def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    station.active(True)
    station.connect(ssid, password)

    while not station.isconnected():
        pass

    print('Connection successful')
    print(station.ifconfig())

# پارامترهای WiFi
ssid = ''
password = ''
connect_to_wifi(ssid, password)

# تنظیم پایه‌ها و PWM
pins = [Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]
pwms = [PWM(p, freq=25000) for p in pins]

# مقدار اولیه PWM برای هر پایه
initial_duty = 512
for pwm in pwms:
    pwm.duty(initial_duty)

# تابعی برای تنظیم PWM
def set_pwm(pin_index, duty):
    if 0 <= pin_index < len(pwms):
        pwms[pin_index].duty(duty)

# ایجاد سرور و گوش دادن به درخواست‌ها
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening on', addr)

# قالب HTML
html = '''<!DOCTYPE html>
<html>
<head>
    <title>ESP32 PWM Control</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #000;
            color: #00aaff;
            text-align: center;
            padding: 50px;
        }}
        h1 {{
            color: #00aaff;
        }}
        form {{
            background: #333;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.5);
            display: inline-block;
            margin-top: 20px;
            width: 400px;
        }}
        .slider-container {{
            display: grid;
            grid-template-columns: 1fr 3fr 1fr;
            align-items: center;
            margin-bottom: 15px;
        }}
        label {{
            font-weight: bold;
            color: #00aaff;
        }}
        input[type="range"] {{
            width: 100%;
            accent-color: #00aaff;
        }}
        .slider-value {{
            margin-left: 10px;
            font-weight: bold;
            width: 50px;
            text-align: right;
            color: #00aaff;
        }}
    </style>
</head>
<body>
    <h1>ESP32 PWM Control</h1>
    <form action="/" method="get">
        <div class="slider-container">
            <label for="master">Set All PWM:</label>
            <input type="range" min="0" max="1023" id="master" onchange="updateAllValues()" value="{pwm_master}">
            <span id="value_master" class="slider-value">{pwm_master}</span>
        </div>
        <div class="slider-container">
            <label for="pwm0">Set PWM for Pin 2:</label>
            <input type="range" min="0" max="1023" name="pwm0" id="pwm0" onchange="updateValue('pwm0')" value="{pwm0}">
            <span id="value_pwm0" class="slider-value">{pwm0}</span>
        </div>
        <div class="slider-container">
            <label for="pwm1">Set PWM for Pin 4:</label>
            <input type="range" min="0" max="1023" name="pwm1" id="pwm1" onchange="updateValue('pwm1')" value="{pwm1}">
            <span id="value_pwm1" class="slider-value">{pwm1}</span>
        </div>
        <div class="slider-container">
            <label for="pwm2">Set PWM for Pin 16:</label>
            <input type="range" min="0" max="1023" name="pwm2" id="pwm2" onchange="updateValue('pwm2')" value="{pwm2}">
            <span id="value_pwm2" class="slider-value">{pwm2}</span>
        </div>
        <div class="slider-container">
            <label for="pwm3">Set PWM for Pin 17:</label>
            <input type="range" min="0" max="1023" name="pwm3" id="pwm3" onchange="updateValue('pwm3')" value="{pwm3}">
            <span id="value_pwm3" class="slider-value">{pwm3}</span>
        </div>
    </form>
    <script>
        function updateValue(id) {{
            var slider = document.getElementById(id);
            var value = document.getElementById('value_' + id);
            value.textContent = slider.value;
            slider.form.submit();  // Submit the form when the slider value changes
        }}
        function updateAllValues() {{
            var masterSlider = document.getElementById('master');
            var masterValue = masterSlider.value;
            document.getElementById('value_master').textContent = masterValue;
            // Update all individual sliders
            var sliders = ['pwm0', 'pwm1', 'pwm2', 'pwm3'];
            sliders.forEach(function(id) {{
                var slider = document.getElementById(id);
                slider.value = masterValue;
                document.getElementById('value_' + id).textContent = masterValue;
            }});
            masterSlider.form.submit();  // Submit the form when the master slider value changes
        }}
    </script>
</body>
</html>
'''

while True:
    cl, addr = s.accept()
    request = cl.recv(1024).decode()
    print('Request:', request)

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

    response = html.format(pwm0=pwm_values[0], pwm1=pwm_values[1], pwm2=pwm_values[2], pwm3=pwm_values[3], pwm_master=initial_duty)
    cl.send('HTTP/1.1 200 OK\r\n')
    cl.send('Content-Type: text/html\r\n')
    cl.send('Connection: close\r\n')
    cl.send(f'Content-Length: {len(response)}\r\n')
    cl.send('\r\n')
    cl.sendall(response)
    cl.close()
