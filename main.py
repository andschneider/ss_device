import socket
import time

import busio
import machine
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA
from send_post import http_post


def get_sensor(seesaw):
    moist = seesaw.moisture_read()
    temp = seesaw.get_temp()
    temp_f = temp * 1.8 + 32
    print("temp: " + str(temp_f) + "  moisture: " + str(moist))
    return moist, temp_f


def get_post_url():
    with open("url.txt", "r") as f_in:
        url = f_in.read().strip()
        print("url", url)
        return url


def main():
    # connect to sensor
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)

    # get the url to hit
    url = get_post_url()

    while True:
        # get sensor readings
        moisture, temperature = get_sensor(ss)
        data = {"sensor_id": 1, "temperature": temperature, "moisture": moisture}

        # send data via http POST
        http_post(url, data)

        # sleep until next post
        time.sleep(60)


main()
