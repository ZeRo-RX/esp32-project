from wifi_connector import WifiConnector
import machine
from machine import Pin , PWM
import socket
from html_generator import HtmlGenerator
import network
from pin_handler import PinHandler
from GY521_SSD1306_i2c_move_and_show import SensorModule
import time

x = 0


class WebServer:
    def __init__(self, WIFI_SSID, WIFI_PASSWORD, pin_numbers):
        self.WIFI_SSID = WIFI_SSID
        self.WIFI_PASSWORD = WIFI_PASSWORD
        self.pin_numbers = pin_numbers
        self.pins = [machine.Pin(pin, machine.Pin.OUT) for pin in pin_numbers]
        self.htmlGenerator = HtmlGenerator(pin_numbers)
        self.html = self.htmlGenerator.create_html()
        self.wifi_connector = WifiConnector(WIFI_SSID, WIFI_PASSWORD)
        self.pin_handler = PinHandler(self.pins, self.pin_numbers)
           
        self.sw1 = Pin(13, Pin.IN, Pin.PULL_DOWN)
        self.sw2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
        
        self.sw3 = Pin(25, Pin.IN, Pin.PULL_DOWN)
        self.sw4 = Pin(26, Pin.IN, Pin.PULL_DOWN)
        self.sw5 = Pin(27, Pin.IN, Pin.PULL_DOWN)

        self.sw1.irq(trigger=Pin.IRQ_RISING, handler=self.handle_sw1)
        self.sw2.irq(trigger=Pin.IRQ_RISING, handler=self.handle_sw2)
        
        self.x1 = 51
        self.x2 = 51
        self.x3 = 51
        self.pwm0 = 0
        self.pwm4 = 0
        self.pwm5 = 0
        
        self.pwm1 = PWM(Pin(33, Pin.OUT), freq=5000, duty=(self.pwm0))
        self.pwm2 = PWM(Pin(15, Pin.OUT), freq=5000, duty=(self.pwm4))
        self.pwm3 = PWM(Pin(23, Pin.OUT), freq=5000, duty=(self.pwm5))

        self.sensor_module = SensorModule()
        
    def handle_sw1(self, pin):
        global x
        print("Key 1 pressed")
        x = 1

    def handle_sw2(self, pin):
        global x
        print("Key 2 pressed")
        x = 0
        
    def handle_web_request(self, conn):
        request = conn.recv(1024)
        request = str(request)

        self.pin_handler.handle_request(request)

        response = "HTTP/1.1 200 OK\nContent-Type: text/html\n\n" + self.html
        conn.send(response)
        conn.close()

    def process_sensor_data(self):
        if self.sw3.value() == 1:
            self.pwm0 += self.x1
            if self.pwm0 >= 1020:
                self.x1 = -51
            if self.pwm0 <= 0:
                self.x1 = 51
            self.pwm1.duty(self.pwm0)
        else:
            pass
        if self.sw4.value() == 1:
            self.pwm4 += self.x2
            if self.pwm4 >= 1020:
                self.x2 = -51
            if self.pwm4 <= 0:
                self.x2 = 51
            self.pwm2.duty(self.pwm4)
        else:
            pass
        if self.sw5.value() == 1:
            self.pwm5 += self.x3
            if self.pwm5 >= 1020:
                self.x3 = -51
            if self.pwm5 <= 0:
                self.x3 = 51
            self.pwm3.duty(self.pwm5)
        else:
            pass
        data = self.sensor_module.read_data()
        self.sensor_module.display_data(data)

    def start_server(self):
        self.wifi_connector.connect()

        addr = network.WLAN().ifconfig()[0]
        print("Web server started on", addr)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((addr, 80))
        s.listen(5)

        while True:
            if x == 1:
                conn, addr = s.accept()
                print("Client connected from", addr)

                self.handle_web_request(conn)
            elif x == 0:
                time.sleep(0.05)
                self.process_sensor_data()