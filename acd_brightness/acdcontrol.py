import usb.core, usb.util, sys, array, logging

sys.argv

Apple = 0x05ac
AppleCinemaDisplay = 0x9226

# find our device
dev = usb.core.find(idVendor=Apple, idProduct=AppleCinemaDisplay)

# was it found?
if dev is None:
    raise ValueError('Device not found')
else:
    print("device " + hex(Apple) + ":" + hex(AppleCinemaDisplay) + " discovered")

cfg = dev[0]
intf = cfg[(0,0)]
ep = intf[0]
dev.set_configuration()

print("reading current brightness value")

# read current value of brightness on ACD
# bmRequestType = 0xA1
# bRequest = 0x01
# wValue = 0x0310
# wIndex = 0x0000
# wLength = 0x0009
currentState = dev.ctrl_transfer(0xA1, 0x01, 0x0310, 0x0000, 0x0009)
brightness = (currentState[1] + (currentState[2] * 255))

print("Current brightness value is " + str(brightness))

newState = (brightness + int(sys.argv[1]))
if (newState > 1019):
    newState = 1019
elif (newState < 0):
    newState = 0

print("New brightness value is " + str(newState))

multiplier = int(newState / 255)
remainder = (newState - (multiplier * 255))

print("output to ACD will be '16, " + str(remainder) + ", " + str(multiplier) + "'")

# bmRequestType = 0x21
# bRequest = 0x009
# wValue = 0x0310
# wIndex = 0x0000
data = array.array('B', [16, remainder, multiplier])
dev.ctrl_transfer(0x21, 0x009, 0x0310, 0x0000, data)

print("brightness done :D")

exit()
