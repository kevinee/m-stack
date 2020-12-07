Vendor Class using Windows Compatible ID (WCID)
-----------------------------------------------

Let's define PnP = plug and play, no user interaction required for device driver install/assignment.

This app creates a PnP device which will be assigned WinUSB as the device driver on Windows 8.1 onwards.
It implements a loopback on two data endpoints of 64-bytes which can be tested from the host using the included Python script.

Just to give some context, here are the options for connecting Windows software to a custom USB device:


* USB CDC class (PnP)

The CDC class enables USB-serial (e.g. RS232) converters to be automatically
assigned to a COM/tty port on the host, without any user interaction. This
is useful for legacy equipment and host software which uses such ports but
for new designs there are better ways (see below).


* Vendor class using custom driver

This method can be PnP if you have signed driver in the Windows store or pre-installed with your software.
But it's difficult and costly to achieve, so you would likely use a USB interface IC from a company who
have done all the hard work, e.g. FTDI which offers COM port or DLL interface.


* HID class (PnP)

Maximum 64,000 bytes/sec full duplex communication, ample for many MCU devices.
Up to two data endpoints (one IN, one OUT) allowed per device.

See https://github.com/libusb/hidapi


* Vendor class using WCID (PnP)

From MS Windows 8.1 onwards, a USB vendor class
device can respond with specific string descriptors which cause it to be
assigned winusb.sys/winusb.dll as the kernel/userspace drivers, with no user
interaction. Your host software can then use winusb.dll directly, or via
libusb for easier API and cross-platform ability. There are some links below [[1]]
to get you started if you want more background information.
Allows full utilisation of USB bandwith and transfer types.
Number of endpoints limited only by your MCU USB peripheral.

For older versions of Windows, you will need to supply a .inf file to link the device with the WinUSB driver.
https://zadig.akeo.ie/ could be used to automatically generate that .inf or install an alternate driver.



[[1]] WCID links

https://docs.microsoft.com/en-us/windows-hardware/drivers/usbcon/automatic-installation-of-winusb

https://github.com/pbatard/libwdi/wiki/WCID-Devices

https://stackoverflow.com/questions/38906880/how-to-work-with-winusb

https://www.silabs.com/community/mcu/32-bit/forum.topic.html/using_microsoft_osd-lMCD

https://github.com/libusb
