import usb.core
import time
import math

# solved problems with libusb installation using
# https://stackoverflow.com/questions/33972145/pyusb-on-windows-8-1-no-backend-available-how-to-install-libusb
# import libusb_package
# for dev in libusb_package.find(find_all=True):
#     print(dev)

idVendor = 0x1044
idProduct = 0x7a3f

dev = usb.core.find(idVendor=idVendor, idProduct=idProduct)
# was it found?
if dev is None:
    raise ValueError('Device not found')
# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

def set_static(color, brightness):
    # TODO do some limits/sanitation checks
    byte_list = []

    # first four bytes common
    byte_list.append('\x08')
    byte_list.append('\x00')
    byte_list.append('\x01')
    byte_list.append('\x01')

    byte_list.extend(['\x00']*4)

    color_byte = ''

    match color:
        case 'RED':
            color_byte = '\x01'
        case 'ORANGE':
            color_byte = '\x05'
        case 'YELLOW':
            color_byte = '\x03'
        case 'GREEN':
            color_byte = '\x02'
        case 'BLUE':
            color_byte = '\x04'
        case 'VIOLET':
            color_byte = '\x06'
        case 'WHITE':
            color_byte = '\x07'
        case _:
            # default WHITE
            color_byte = '\x07'

    bright_5 = brightness//10 * 5

    byte_list[4] = chr(bright_5)
    byte_list[5] = color_byte
    byte_list[6] = '\x01' # seventh byte also common
    byte_list[7] = chr(244 - ord(color_byte) - bright_5)

    msg = ''.join(byte_list)
    # print(":".join("{:04x}".format(ord(c)) for c in msg))

    dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0300, wIndex=3, data_or_wLength=msg)

def set_mode(mode):
    # TODO do some limits/sanitation checks
    msg = ''

    match mode:
        case 'STATIC':
            # only static white full brightness set here
            # for more options use the set_static method
            msg = '\x08\x00\x01\x01\x32\x07\x01\xbb'
        case 'BREATHING':
            msg = '\x08\x00\x02\x05\x32\x01\x01\xbc'
        case 'WAVE_RANDOM':
            msg = '\x08\x00\x03\x08\x32\x08\x04\xae'
        case 'WAVE_OFF':
            msg = '\x08\x00\x03\x08\x00\x08\x04\xe0'
        case 'FADE_ON_KEYPRESS':
            msg = '\x08\x00\x04\x01\x32\x08\x01\xb7'
        case 'MARQUEE':
            msg = '\x08\x00\x05\x05\x32\x01\x01\xb9'
        case 'RIPPLE':
            msg = '\x08\x00\x06\x05\x32\x01\x01\xb8'
        case 'FLASH_ON_KEYPRESS':
            msg = '\x08\x00\x07\x05\x32\x01\x01\xb7'
        case 'NEON':
            msg = '\x08\x00\x08\x05\x32\x08\x01\xaf'
        case 'RAINBOW_MARQUEE':
            msg = '\x08\x00\x09\x05\x32\x08\x01\xae'
        case 'RAINDROP':
            msg = '\x08\x00\x0a\x05\x32\x08\x01\xad'
        case 'CIRCLE_MARQUEE':
            msg = '\x08\x00\x0b\x05\x32\x01\x01\xb3'
        case 'HEDGE':
            msg = '\x08\x00\x0c\x05\x32\x01\x01\xb2'
        case 'ROTATE':
            msg = '\x08\x00\x0d\x05\x32\x01\x01\xb1'
        case _:
            # default STATIC
            msg = '\x08\x00\x01\x01\x32\x07\x01\xbb'

    dev.ctrl_transfer(bmRequestType=0x21, bRequest=0x09, wValue=0x0300, wIndex=3, data_or_wLength=msg)

def color_demo(color, num_loops, speed):
    # speed = 1 to 10, 10 being fastest

    diff = -10
    brightness = 0
    current_loop = 0
    for i in range(100):
        if i % 10 == 0:
            diff *= -1
            current_loop += 1
            if current_loop > num_loops:
                return
        brightness += diff
        set_static(color, brightness)
        time.sleep(0.2 / speed)

def mode_demo():
    set_mode('STATIC')
    time.sleep(5)
    set_mode('BREATHING')
    time.sleep(5)
    set_mode('WAVE_RANDOM')
    time.sleep(5)
    set_mode('WAVE_OFF')
    time.sleep(5)
    set_mode('FADE_ON_KEYPRESS')
    time.sleep(5)
    set_mode('FLASH_ON_KEYPRESS')
    time.sleep(5)
    set_mode('RAINBOW_MARQUEE')
    time.sleep(5)
    set_mode('RAINDROP')
    time.sleep(5)
    set_mode('CIRCLE_MARQUEE')
    time.sleep(5)
    set_mode('HEDGE')
    time.sleep(5)
    set_mode('ROTATE')

# color_demo('RED', 2, 2)
# color_demo('ORANGE', 2, 5)
# color_demo('YELLOW', 2, 10)
# color_demo('GREEN', 2, 1)
# color_demo('BLUE', 2, 6)
# color_demo('VIOLET', 2, 2)
# color_demo('WHITE', 2, 8)

# mode_demo()