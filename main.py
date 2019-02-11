import machine
import socket
import time

from board import SCL, SDA
import busio

from adafruit_seesaw.seesaw import Seesaw


def get_sensor(seesaw):
    moist = seesaw.moisture_read()
    temp = seesaw.get_temp()
    temp_f = temp * 1.8 + 32
    print("temp: " + str(temp_f) + "  moisture: " + str(moist))
    return moist, temp_f


def create_server():
    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("listening on", addr)
    return s


def update_data(server, seesaw):
    html = """<!DOCTYPE html>
    <html>
        <head> <title>yeet</title> </head>
        <body> <h1>soil sensor!</h1>
            <table border="1"> <tr><th>Temp</th><th>Moist</th></tr> %s </table>
        </body>
    </html>
    """
    while True:
        # connection
        cl, addr = server.accept()
        print("client connected from", addr)
        cl_file = cl.makefile("rwb", 0)

        # get sensor readings
        moisture, temperature = get_sensor(seesaw)

        # not sure
        while True:
            line = cl_file.readline()
            if not line or line == b"\r\n":
                break

        row = ["<tr><td>%s</td><td>%s</td></tr>" % (str(temperature), str(moisture))]
        response = html % "\n".join(row)
        cl.send(response)
        cl.close()


def main():
    # connect to sensor
    i2c_bus = busio.I2C(SCL, SDA)
    ss = Seesaw(i2c_bus, addr=0x36)

    # create simple server
    server = create_server()

    # update and send data to webpage
    update_data(server, ss)


main()
