import network

class WifiConnector:
    def __init__(self, ssid, password):
        self.ssid = ssid
        self.password = password
        self.wlan = network.WLAN(network.STA_IF)
        
    def connect(self):
        self.wlan.active(True)
        self.wlan.connect(self.ssid, self.password)
        while not self.wlan.isconnected():
            pass
        print("Connected to WiFi")
