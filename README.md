# ss_device
IoT soil moisture sensor using CircuitPython  

## General
Built upon the wonderful Adafruit ecosystem, this small project utilizes CircuitPython[1] (a port of MicroPython), a ESP8266 WiFi enabled board, and a capacitive sensor to monitor soil moisture. Right now, it simply creates a local server and posts the moisture and temperature readings. In the future, it will connect to an API and send data to a database for monitoring. 

## Hardware components
Board: [Adafruit Feather HUZZAH with ESP8266](https://www.adafruit.com/product/2821)    
Sensor: [Adafruit STEMMA Soil Sensor](https://www.adafruit.com/product/4026)

## Software dependencies
 - [seesaw](https://github.com/adafruit/Adafruit_CircuitPython_seesaw)
 - [BusDevice](https://github.com/adafruit/Adafruit_CircuitPython_BusDevice)

## Installing CircuitPython and working with the board
1) First thing is to flash the latest firmware of CircuitPython, which can be found [here](https://github.com/adafruit/circuitpython/releases/latest). I would recommend following the guide from Adafruit, [here](https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-for-esp8266). 

2) Next, make sure you have `ampy`[2] installed and connect to the board like so:
    ```sh
    $ ampy --port /dev/ttyUSB0 ls
    ```
    This should show you the files that are currently loaded on the board. After a fresh firmware flash you should only have `boot.py`.

3) Now it is time to copy over the dependencies. First, create a directory called `lib` on the board:
    ```sh
    $ ampy --port /dev/ttyUSB0 mkdir lib
    ```
    Next, copy over the two libraries from Adafruit:
    ```sh
    $ ampy --port /dev/ttyUSB0 put adafruit_seesaw /lib
    $ ampy --port /dev/ttyUSB0 put adafruit_bus_device /lib
    ```
4) Test the sensor is working by running the `test_sensor.py` file:
    ```sh
    $ ampy --port /dev/ttyUSB0 run --no-output test_sensor.py
    ```
    Using the `--no-output` flag will run the script in the background on the board. You will have to connect to the REPL to see it’s output. I use `picocom`[3], which can be installed through apt, like so `sudo apt install picocom`. Now, let’s see the REPL:
    ```sh
    $ picocom /tty/USB0 -b115200
    ```

## Connecting to WiFI and reading sensor data
1) First, create your WiFi settings file and connect to the network. The file IO is pretty minimal in CircuitPython, so the settings file is a simple text file with two lines. The first line is the network name and the second line is the password. The `wifi.txt` thus looks like:

    ```
    ssid
    password
    ```
    Now, copy over the `wifi.txt` and `boot.py` to the board using ampy:
    ```sh
    $ ampy --port /tty/USB0 put wifi.txt
    $ ampy --port /tty/USB0 put boot.py
    ```
    Next, connect to the REPL using `picocom` and then reset the board. You should see a connection readout. The `boot.py` is ran on every start or reset of the board, so it will now connect to your WiFi automatically. 

2) Finally, copy over the `main.py` file. This file gets ran on every start or reset, but after the `boot.py` file.
    ```sh
    $ ampy --port /tty/USB0 put main.py
    ```
    This script will read the sensor, create a http server on your local network, and print the sensor data to the server. Simply go the IP address that is printed to the REPL. Every page refresh gets new data from the sensor. 


---
[1] [CircuitPython](https://circuitpython.readthedocs.io/en/3.x/)    
[2] [ampy](https://github.com/pycampers/ampy)    
[3] [picocom](https://github.com/npat-efault/picocom)
