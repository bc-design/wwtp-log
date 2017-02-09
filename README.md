# wwtp-log

Interfacing a bunch of sensors in Ubuntu Linux

## Networking

IP address was initially 70.199.11.133.  To determine the current IP address: 

  curl ipinfo.io/ip



## Dissolved Oxygen (DO) Probe

Dissolved oxygen is measured with an Insight IG Model 2000 Mixed Liquor Analyzer.

This device uses the MODBUS communication protocol.

MinimalModbus 0.7
+ "Easy-to-use Modbus RTU and Modbus ASCII implementation for Python"
+ https://pypi.python.org/pypi/MinimalModbus

PyModbus
+ "full Modbus protocol implementation"
+ https://pymodbus.readthedocs.io/en/latest/
+ https://pypi.python.org/pypi/pymodbus
+ https://github.com/bashwork/pymodbus
+ https://apps.ubuntu.com/cat/applications/raring/python-pymodbus/

libmodbus
+ "a fast and portable Modbus library"
+ http://manpages.ubuntu.com/manpages/xenial/man7/libmodbus.7.html

Modbus Tutorial for Arduino, Raspberry Pi and Intel Galileo
+ https://www.cooking-hacks.com/documentation/tutorials/modbus-module-shield-tutorial-for-arduino-raspberry-pi-intel-galileo/

"The Modbus protocol can be implemented over RS-485 and RS-232 phisical layers. Cooking-Hacks provides the necesary hardware and software for working with both protocols. The name and use of the functions are the same for RS-232 and RS-485, and the only changes are the library to include and the instantiation of the object. The diferences between the two standards are explained in the corresponding tutorials."


http://www.insiteig.com/model-2000-dual-channel-process-analyzer.htm
http://www.insiteig.com/pdfs/SPECS%20FOR%20MODEL%202000%20WITH%20MODEL%2010%20AND%2015.PDF
Modbus RTU
RS-232
0-20mA or 4-20mA
Documentation: Operator Manual, Packing list, Modbus RTU Appendix

The good stuff:
http://www.insiteig.com/pdfs/Model-2000CE-Manual-13-July-16.pdf

Messages start with a silent interval of at least 3.5 character times
followed by 4 fields and then
followed by another silent interval of at least 3.5 character times.

The first field contains the device address.						1 byte
The second field contains the function code. 						1 byte
The third field contains the data. 									1+ bytes
The fourth field contains the CRC value. 							2 bytes
Each byte has 1 start bit, 8 data bits, no parity, and 1 stop bit.

Address field
The address field contains one byte. Valid slave device addresses are in range 1 to 247 decimal.

Function code field
The function code field contains one byte. See the section titled Function codes supported by the
Model 2000.

Data field
The data field contains one or more byte. This information is used by the analyzers to take the action
defined by the function code.

CRC field
The CRC (cyclical redundancy check) field is two bytes, containing a 16-bit binary value. The CRC
value is calculated by the transmitting device, which appends the CRC to the message. The receiving
device recalculates a CRC during receipt of the message, and compares the calculated value to the actual
value it received in the CRC field. If the two values are not equal, the message will be discarded.

Query
Below is an example of a request to report the ID and status of slave address 1.
Field Name Example
Slave Address 01
Function 11
CRC --

The normal response of the Model 2000 is shown below.
Field Name Example
Slave Address 01
Function 11
Byte Count 04
Slave ID 02
Run status 00=Off, FF = On
Ch 1 sensor type 00=Model 10
10=Model 15
20=Model 15L
30=Model M51
31=Model M52
Ch 2 sensor type 00=Model 10
10=Model 15
20=Model 15L
30=Model M51
31=Model M52
CRC --

Below is an example of a request to read the channel 2 status and channel 2 primary measurement
registers from an analyzer with the slave address of 1.
Field Name Example
Slave Address 01
Function 04
Starting Address Hi 00
Starting Address Lo 03
No. of Regs. Hi 00
No. of Regs. Lo 03
CRC --

Below is an example of a response to the previous query where channel 2 is connected to a Model 10
D.O. sensor measuring 8.3 ppm at 25.0°C.
Field Name Example
Slave Address 01
Function 04
Byte Count 06
Data Hi (Reg 3) 00
Data Lo (Reg 3) 00
Data Hi (Reg 4) 03
Data Lo (Reg 4) 3E
Data Hi (Reg 5) 00
Data Lo (Reg 5) FA
CRC --

The Model 10 sensor will report D.O. as the primary measurement and temperature as the secondary
measurement. The units for D.O. are hundredths of ppm and the units for temperature are tenths of °C.

The query message specifies the starting register address and the quantity of registers to be read. The
Model 2000 input registers are as follows:
Address Register
0000 			Channel 1 status
0001 			Channel 1 primary measurement
0002 			Channel 1 secondary measurement
0003 			Channel 2 status
0004 			Channel 2 primary measurement
0005 			Channel 2 secondary measurement
000A 			Last 4 digits of the channel 1 sensor serial number
000F 			Last 4 digits of the channel 2 sensor serial number
The channel status is reported as follows:
Status Description
0000 Normal
0001 Sensor not responding
0002 Sensor error
0003 Sensor requires a zero calibration (Model 15/15L only)

## Function Codes

### 01 - Read Coil Status

### 04 - Read Input Registers

### 06 - Preset Single Register

### 17 - Report Slave ID
