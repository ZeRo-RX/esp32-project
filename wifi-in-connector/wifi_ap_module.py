import network

class WifiAPManager:
    def __init__(self, WIFI_SSID, WIFI_PASSWORD):
        self.WIFI_SSID = WIFI_SSID
        self.WIFI_PASSWORD = WIFI_PASSWORD
        self.ap = network.WLAN(network.AP_IF)

    def create_wifi_ap(self):
        self.ap.active(True)
        self.ap.config(essid=self.WIFI_SSID, password=self.WIFI_PASSWORD)
        print("WiFi Access Point created:", self.WIFI_SSID)
