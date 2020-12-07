import usb.core
import usb.util
import sys,time
import os

'''
Step 1:
Install libusb, download the latest release 7zip archive which has prebuilt DLL
https://github.com/libusb/libusb/releases
Copy libusb-1.0.dll to somewhere on your path, e.g. Windows/System32/

Step 2:
Install python
Install bindings for libusb with the command line:
pip install pyusb

Step 3:
Make sure your PIC is running the attached example firmware.
Check device listed in Device Manager.
Check VID/PID matches.
When you are experimenting, if a device repond on first connect to WCID 0xEE string request,
Windows will likely make a note of it in the registry and stop it working
after you fix firmware. From docs/winusb.txt:

Windows will only read the Microsoft-specific descriptors the first time the
device is connected, which is undesirable during development of a WinUSB
device.  Windows can be forced to re-read the descriptors by performing the
following steps:
	1. In the Device Manager, right-click the device (which will show
	   as "WinUSB Device" under "Universal Serial Bus Devices") and
	   select "Uninstall." This will unbind the driver.
	2. In the registry, delete the section associated with your device in
	   Computer\\HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Control\\usbflags\\VID_PID
	   The device keys in UsbFlags begin with the VID and PID of the
	   device they describe.
	3. Disconnect and re-connect your device. The next time the device
	   is connected, Windows will request the WinUSB descriptors.


Step 4:
Run this script and you should see some output like this:

Manufacturer: Signal 11 Software LLC.
Product:      USB Stack Test Device
Serial:       12345678
Endpoint 1 loopback:  202 kbytes/sec
Endpoint 2 loopback:  198 kbytes/sec

'''

#https://github.com/pyusb/pyusb/blob/master/docs/tutorial.rst
#https://pid.codes/howto/

VENDOR_ID =  0x1209
PRODUCT_ID = 0x000E

dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if dev is None:
    raise ValueError('Device not found.')
    sys.exit(1)

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

#print(dev) #show all device info

str_manuf = usb.util.get_string(dev, dev.iManufacturer)
str_product = usb.util.get_string(dev, dev.iProduct)
str_serial = usb.util.get_string(dev, dev.iSerialNumber)
print('Manufacturer: ' + str_manuf)
print('Product:      ' + str_product)
print('Serial:       ' + str_serial)


msg = os.urandom(64) #packet size is 64 bytes
npkts=2000

start = time.perf_counter()
for i in range(npkts):
    dev.write(0x01, msg) #To endpoint 1_OUT write msg with 100ms timeout
    ret = dev.read(0x81, 64, 100) #From endpoint 1_IN read 64 bytes with 100ms timeout
    #sret = ''.join([chr(x) for x in ret])
    #print(''.join('{:02X} '.format(a) for a in ret))
finish = time.perf_counter()
print('Endpoint 1 loopback: ', int((64*npkts)/(finish-start)/1024), 'kbytes/sec')

start = time.perf_counter()
for i in range(npkts):
    dev.write(0x02, msg, 100) #To endpoint 1_OUT write msg with 100ms timeout
    ret = dev.read(0x82, 64, 100) #From endpoint 1_IN read 64 bytes with 100ms timeout
    #sret = ''.join([chr(x) for x in ret])
    #print(''.join('{:02X} '.format(a) for a in ret))
finish = time.perf_counter()
print('Endpoint 2 loopback: ', int((64*npkts)/(finish-start)/1024), 'kbytes/sec')


sys.exit(1)
