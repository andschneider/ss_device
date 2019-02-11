import gc
import network

gc.collect()


def get_wifi_settings():
    with open("wifi.txt", "r") as f_in:
        wifi = f_in.read().split("\n")
        return wifi[0], wifi[1]


def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    # get credentials
    ssid, pw = get_wifi_settings()

    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(ssid, pw)
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())


do_connect()
