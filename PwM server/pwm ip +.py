import network
import uasyncio as asyncio
from machine import Pin, PWM
import socket

# اطلاعات وای‌فای خود را وارد کنید
ssid = ''
password = ''

# تنظیم پایه‌ها و PWM
pins = [Pin(2, Pin.OUT), Pin(4, Pin.OUT), Pin(16, Pin.OUT), Pin(17, Pin.OUT)]
pwms = [PWM(p, freq=25000) for p in pins]

# مقدار اولیه PWM برای هر پایه
for pwm in pwms:
    pwm.duty(512)

# تنظیمات IP ثابت
ip = '192.168.1.32'
subnet = '255.255.255.0'
gateway = '192.168.1.1'
dns = '8.8.8.8'

wlan = None  # تعریف متغیر global برای wlan

async def connect_wifi():
    global wlan
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((ip, subnet, gateway, dns))
    wlan.connect(ssid, password)

    for _ in range(10):  # حداکثر 10 بار تلاش برای اتصال
        if wlan.isconnected():
            print('اتصال برقرار شد!')
            print('اطلاعات شبکه:', wlan.ifconfig())
            return wlan
        print('در حال اتصال...')
        await asyncio.sleep(1)

    print('اتصال برقرار نشد')
    return None

async def check_connection():
    global wlan
    while True:
        if not wlan.isconnected():
            print('اتصال قطع شد! در حال تلاش برای اتصال مجدد...')
            wlan = await connect_wifi()
            if wlan is None:
                print('عدم موفقیت در اتصال مجدد. لطفاً تنظیمات را بررسی کنید.')
            else:
                print('اتصال مجدداً برقرار شد.')
        else:
            print('اتصال برقرار است.')

        await asyncio.sleep(5)  # هر 5 ثانیه وضعیت اتصال را بررسی می‌کنیم

async def web_server():
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
        input[type="number"] {{
            width: 100px;
            margin: 0 auto;
            display: block;
            color: #00aaff;
            background-color: #000;
            border: 1px solid #00aaff;
            border-radius: 5px;
            padding: 5px;
            font-size: 16px;
            text-align: center;
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
            <label for="master">All PWM:</label>
            <input type="range" min="0" max="1023" id="master" onchange="updateAllValues()" value="{pwm_master}">
            <span id="value_master" class="slider-value">{pwm_master}</span>
        </div>
        <div class="slider-container">
            <label for="pwm0">PWM Pin 2:</label>
            <input type="range" min="0" max="1023" name="pwm0" id="pwm0" onchange="updateValue('pwm0')" value="{pwm0}">
            <span id="value_pwm0" class="slider-value">{pwm0}</span>
        </div>
        <div class="slider-container">
            <label for="pwm1">PWM Pin 4:</label>
            <input type="range" min="0" max="1023" name="pwm1" id="pwm1" onchange="updateValue('pwm1')" value="{pwm1}">
            <span id="value_pwm1" class="slider-value">{pwm1}</span>
        </div>
        <div class="slider-container">
            <label for="pwm2">PWM Pin 16:</label>
            <input type="range" min="0" max="1023" name="pwm2" id="pwm2" onchange="updateValue('pwm2')" value="{pwm2}">
            <span id="value_pwm2" class="slider-value">{pwm2}</span>
        </div>
        <div class="slider-container">
            <label for="pwm3">PWM Pin 17:</label>
            <input type="range" min="0" max="1023" name="pwm3" id="pwm3" onchange="updateValue('pwm3')" value="{pwm3}">
            <span id="value_pwm3" class="slider-value">{pwm3}</span>
        </div>
        <div class="slider-container" style="grid-template-columns: 1fr 2fr 1fr;">
            <label for="input_pwm">All PWM Value:</label>
            <input type="number" min="0" max="1023" id="input_pwm" onchange="updateFromInput()" value="{pwm_master}">
            <span id="value_input_pwm" class="slider-value">{pwm_master}</span>
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
            document.getElementById('input_pwm').value = masterValue;
            // Update all individual sliders
            var sliders = ['pwm0', 'pwm1', 'pwm2', 'pwm3'];
            sliders.forEach(function(id) {{
                var slider = document.getElementById(id);
                slider.value = masterValue;
                document.getElementById('value_' + id).textContent = masterValue;
            }});
            masterSlider.form.submit();  // Submit the form when the master slider value changes
        }}
        function updateFromInput() {{
            var inputField = document.getElementById('input_pwm');
            var inputValue = inputField.value;
            document.getElementById('value_input_pwm').textContent = inputValue;
            document.getElementById('master').value = inputValue;
            updateAllValues();
        }}
    </script>
</body>
</html>
'''

    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Request:', request)

        # استخراج مقادیر PWM از درخواست
        pwm_values = [pwms[i].duty() for i in range(4)]  # مقدار پیش‌فرض برابر با مقدار فعلی
        pwm_master = None
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

        master_str = 'master='
        master_start = request.find(master_str)
        if master_start != -1:
            try:
                pwm_master = int(request[master_start + len(master_str):].split(' ')[0].split('&')[0])
                if 0 <= pwm_master <= 1023:
                    pwm_values = [pwm_master] * 4
                    for i in range(4):
                        set_pwm(i, pwm_master)
            except ValueError:
                pass

        input_pwm_str = 'input_pwm='
        input_pwm_start = request.find(input_pwm_str)
        if input_pwm_start != -1:
            try:
                pwm_master = int(request[input_pwm_start + len(input_pwm_str):].split(' ')[0].split('&')[0])
                if 0 <= pwm_master <= 1023:
                    pwm_values = [pwm_master] * 4
                    for i in range(4):
                        set_pwm(i, pwm_master)
            except ValueError:
                pass

        if pwm_master is None:
            pwm_master = max(pwm_values)

        response = html.format(pwm0=pwm_values[0], pwm1=pwm_values[1], pwm2=pwm_values[2], pwm3=pwm_values[3], pwm_master=pwm_master)
        cl.send('HTTP/1.1 200 OK\r\n')
        cl.send('Content-Type: text/html\r\n')
        cl.send('Connection: close\r\n')
        cl.send(f'Content-Length: {len(response)}\r\n')
        cl.send('\r\n')
        cl.sendall(response)
        cl.close()

async def main():
    global wlan
    wlan = await connect_wifi()

    if wlan:
        await asyncio.gather(check_connection(), web_server())

asyncio.run(main())
