#!/usr/bin/env python3

import minimalmodbus
import serial
import time
import datetime
import subprocess

mydelay = 1
myunits = 'lb'

usbscale = serial.Serial('/dev/usbscale',
                      baudrate=9600,
                      bytesize=serial.EIGHTBITS,
                      parity=serial.PARITY_NONE,
                      stopbits=serial.STOPBITS_ONE,
                      timeout=1,
                      xonxoff=0,
                      rtscts=0
                      )

def scale_getweight():
    while True:
        usbscale.write("*P".encode('utf8'))
        reading = usbscale.readline().decode('utf8')
        if len(reading) > 0:
            value, units = reading.split()
            if (units == myunits):
                return value
            else:
                #print("units are {}; changing units...".format(units))
                scale_changeunits()
        else:
            time.sleep(1)

def scale_changeunits():
    usbscale.write("*C".encode('utf8'))
    time.sleep(1)

def scale_getweight_workaround():
    myval = ''
    myproc = subprocess.Popen(["printreq"], stdout=subprocess.PIPE)
    try:
        myval = myproc.communicate(timeout=1)[0].decode('utf8').strip()
    except:
        pass
    return myval

def scale_changeunits_workaround():
    time.sleep(1)
    subprocess.run(["unitchange"])
    time.sleep(1)

probetrans = minimalmodbus.Instrument('/dev/probetrans', 1)
probetrans.serial.baudrate = 9600
probetrans.serial.timeout = 1.0

mycurrent = "current.log"
myfile = "{}.log".format(datetime.datetime.today().isoformat()[:16])

with open(myfile,'w+') as mylog, open(mycurrent,'a') as mycurrent:
    val_scale = ''
    val_temp = ''
    val_do = ''
    val_relay = ['','','','']

    while True:
        ts = time.time()
        try:
            val_scale = scale_getweight()
        except:
            #print("ERROR: scale_getweight")
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
            #print("ERROR: probetrans_read")
            pass

        myline = "{:.2f},{!s},{:0.2},{!s},{!s}\n".format(ts,val_temp,val_do,val_scale,val_relay[0])
        #print(myline, end='')

        if len(val_scale) != 0:
            mylog.write(myline)
            mylog.flush()
            mycurrent.write(myline)
            mycurrent.flush()
        time.sleep(mydelay)

