#!/usr/bin/env python3

import minimalmodbus
#import serial
import time
import datetime
import subprocess

mydelay = 1
myunits = 'g'

"""
usbscale = serial.Serial('/dev/usbscale',
                      baudrate=57600,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=1,
                      xonxoff=0,
                      rtscts=0
                      )
"""

def scale_getweight():
    myval = ''
    myproc = subprocess.Popen(["printreq"], stdout=subprocess.PIPE)
    try:
        myval = myproc.communicate(timeout=1)[0].decode('utf8').strip()
    except:
        pass
    return myval

def scale_changeunits():
    time.sleep(1)
    subprocess.run(["unitchange"])
    time.sleep(1)

probetrans = minimalmodbus.Instrument('/dev/probetrans', 1)
probetrans.serial.baudrate = 9600
probetrans.serial.timeout = 1.0

myfile = "current.log"
#myfile = "{}.log".format(datetime.datetime.today().isoformat()[:16])

while True:
    reading = scale_getweight()
    if (reading != ''):
        units = reading.split()[1]
        print(units)
        if (units == myunits):
            break
        else:
            scale_changeunits()
    else:
        time.sleep(1)

with open(myfile,'a') as mylog:
    val_scale = ''
    val_temp = ''
    val_do = ''
    val_relay = ['','','','']

    while True:
        ts = time.time()
        try:
            scale_reading = scale_getweight()
            if len(scale_reading) != 0:
                val_scale = scale_reading.split()[0]
        except:
            pass

        try:
            val_do = probetrans.read_register(registeraddress=1,
                                                numberOfDecimals=2,
                                                functioncode=4,
                                                signed=True)
            time.sleep(1)
            val_temp = probetrans.read_register(registeraddress=2,
                                              numberOfDecimals=1,
                                              functioncode=4,
                                              signed=True)
            for i in range(0,4):
                val_relay[i] = probetrans.read_bit(registeraddress=i,
                                            functioncode=1)

        except:
            pass;
        myline = "{:.2f},{!s},{:0.2},{!s},{!s}\n".format(ts,val_temp,val_do,val_scale,val_relay[0])
        print(myline, end='')

        if len(val_scale) != 0:
            mylog.write(myline)
            mylog.flush()
        time.sleep(mydelay)

