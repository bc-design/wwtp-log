#!/usr/bin/env python3

import minimalmodbus
import serial
import time
import datetime

mydelay = 1
myunits = 'g'

usbscale = serial.Serial('/dev/usbscale',
                      baudrate=57600,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=1,
                      xonxoff=0,
                      rtscts=0
                      )

probetrans = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
probetrans.serial.baudrate = 9600
probetrans.serial.timeout = 1.0

myfile = datetime.datetime.today().isoformat()[:16]

while True:
    usbscale.write("*P".encode('utf8'))
    time.sleep(0.1)
    u = usbscale.readline().decode('utf8').split()[-1]
    if (u == myuints):
        break
    time.sleep(0.1)
    usbscale.write("*C".encode('utf8'))


with open(myfile,'w') as mylog:
    while True:
        ts = time.time()
        usbscale.write("*P".encode('utf8'))
        val_scale = ' '.join(usbscale.readline().decode('utf8').split())
        val_temp = probetrans.read_register(registeraddress=1,
			                    numberOfDecimals=1,
                                            functioncode=4,
                                            signed=True)
        val_do = probetrans.read_register(registeraddress=2,
                                          numberOfDecimals=3,
                                          functioncode=4,
                                          signed=True)
        myline = "{:.2f}, {!s} \u00B0C, {:.2} ppm, {}\n".format(ts,val_temp,val_do,val_scale)
        mylog.write(myline)
        mylog.flush()
        time.sleep(mydelay)
