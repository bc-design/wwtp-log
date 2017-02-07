#!/usr/bin/env python3

import minimalmodbus as mm

for add in [1]:
# for add in range(0,247):
    for baud in [9600]:
#    for baud in [300,1200,2400,4800,9600,14400,19200,28800,38400,57600,115200]:
        instrument = mm.Instrument(port='/dev/ttyUSB0', slaveaddress=add)
        instrument.serial.timeout = 1.00
        instrument.serial.baudrate = baud
        #print(instrument)

        for reg in range(0,5):
            try:
                print(instrument.read_register(registeraddress=reg, functioncode=4))
                print(instrument)
            except IOError:
                #print("Failed to read from instrument at {}".format(instrument.address))
                print('.', end='', flush=True)
