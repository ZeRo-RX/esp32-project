import network
essid='ESP32_AP'
password='12345678'

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid, password)
print('AP IP:', ap.ifconfig()[0])
