import network
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid='ESP32_AP')
ap.config(password='')
print('AP IP:', ap.ifconfig()[0])