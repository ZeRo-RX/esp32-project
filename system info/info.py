import network
import socket
import OLED
from machine import SoftI2C, Pin

i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled = OLED.SSD1306_I2C(128, 64, i2c)

def connect_to_wifi(ssid, password):
    wifi = network.WLAN(network.STA_IF)
    if not wifi.isconnected():
        wifi.active(True)
        wifi.connect(ssid, password)
        while not wifi.isconnected():
            pass
    return wifi

def start_tcp_server(wifi, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((wifi.ifconfig()[0], port))
    server_socket.listen(1)
    print('TCP Server started on {}:{}'.format(wifi.ifconfig()[0], port))
    return server_socket

def main():
    your_wifi_ssid = ''
    your_wifi_password = ''
    tcp_port = 80

    wifi = connect_to_wifi(your_wifi_ssid, your_wifi_password)
    server_socket = start_tcp_server(wifi, tcp_port)

    while True:
        try:
            client_socket, client_address = server_socket.accept()
            data = client_socket.recv(1024).decode()
            cpu, gpu = data.split('\n')
            oled.text(cpu, 0, 0)
            oled.text(gpu, 0, 15)
            oled.show()
            oled.fill(0)
        finally:
            client_socket.close()

if __name__ == "__main__":
    main()
