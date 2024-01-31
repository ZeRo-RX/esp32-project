import time
import network
import socket
from machine import Pin

# Set the
ssid = "ZeRo"
password = "karimi1397"

# Starting WiFi module
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

# Connection WiFi module to the network
wlan.connect(ssid, password)

# Waiting for WiFi module to connect to the network
while not wlan.isconnected():
    pass

# Setting D2 as the out module
pin2 = Pin(2, Pin.OUT)

# starting simple web service
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 80))
server.listen(1)


def render(pin_state):
    # Rendering HRML content for the web service
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

# Port 2 value at the beginning
state = "off"

while True:
    # Accepting new connection
    connection, address = server.accept()

    # Getting the request from client
    request = connection.recv(1024)

    # Processing Request
    if "GET /on HTTP/1.1" in request:
        # Turning on web port 2
        state = "on"
        pin2.on()

    elif "GET /off HTTP/1.1" in request:
        # Turning off web port 2
        state = "off"
        pin2.off()

    #Sending response to the client
    response = render(state)
    connection.send(response.encode())

    # Closing connection
    connection.close()

