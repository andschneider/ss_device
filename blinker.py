import time
import machine


led = machine.Pin(15, machine.Pin.OUT)
while True:
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)
