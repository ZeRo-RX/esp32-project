import network

SSID = ''
PASSWORD = ''



wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID,PASSWORD)
while not wlan.isconnected():
    pass
print('IP:', wlan.ifconfig()[0])
