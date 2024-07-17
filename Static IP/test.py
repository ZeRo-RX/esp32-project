import network
import time

# اطلاعات وای‌فای خود را وارد کنید
ssid = ''
password = ''

# تنظیمات IP ثابت
ip = '192.168.1.8'
subnet = '255.255.255.0'
gateway = '192.168.1.1'
dns = '8.8.8.8'

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.ifconfig((ip, subnet, gateway, dns))
    wlan.connect(ssid, password)

    # تلاش برای اتصال به وای‌فای
    for _ in range(10):  # حداکثر 10 بار تلاش برای اتصال
        if wlan.isconnected():
            #print('اتصال برقرار شد!')
            #print('اطلاعات شبکه:', wlan.ifconfig())
            return wlan
        #print('در حال اتصال...')
        time.sleep(1)

    #print('اتصال برقرار نشد')
    return None

def main():
    wlan = connect_wifi()
    if wlan is None:
        return

    while True:
        if not wlan.isconnected():
            #print('اتصال قطع شد! در حال تلاش برای اتصال مجدد...')
            wlan = connect_wifi()
            if wlan is None:
                #print('عدم موفقیت در اتصال مجدد. لطفاً تنظیمات را بررسی کنید.')
                break
        else:
            print('اتصال برقرار است.')

        time.sleep(1)  # هر 5 ثانیه وضعیت اتصال را بررسی می‌کنیم

if __name__ == "__main__":
    main()
