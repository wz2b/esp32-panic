# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)

import webrepl
import network
import ubinascii
from machine import Pin
import lptest
	
webrepl.start()

nic = network.WLAN(network.STA_IF)
mac = ubinascii.hexlify(nic.config('mac'),':').decode()

nic.active(True)
nic.connect('FROGPOND-IOT', 'b7iqiwUB')



safe_pin = Pin(4, Pin.IN, Pin.PULL_UP)
if safe_pin.value() == 0:
    lptest.run()


