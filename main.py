import socket
import time

import busio
import machine
from adafruit_seesaw.seesaw import Seesaw
from board import SCL, SDA
from api_requests import get_auth, post_data


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


def get_api_credentials():
    with open("credentials.txt", "r") as f_in:
        creds = f_in.read().split("\n")
        return creds[0], creds[1]


def main():
    # connect to sensor
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)

    # get the url to hit and api credentials
    url = get_post_url()
    api_user, api_pass = get_api_credentials()

    while True:
        # get sensor readings
        moisture, temperature = get_sensor(ss)
        data = {"sensor_id": 2, "temperature": temperature, "moisture": moisture}

        # login to api
        token = get_auth(url, credentials={"username": api_user, "password": api_pass})

        # send sensor data
        if token:
            post_data(url, token, data)

        # sleep until next post
        time.sleep(60)


main()
