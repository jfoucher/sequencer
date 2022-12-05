import board
import digitalio
import storage
import usb_hid, usb_midi
import usb_cdc
import displayio
import busio
import time
import adafruit_displayio_ssd1306
import adafruit_imageload
#splash screen

displayio.release_displays()

# Use for I2C
i2c = busio.I2C(scl=board.GP21, sda=board.GP20)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 32


display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT, rotation=180)

splash = displayio.Group()
display.show(splash)

odb = displayio.OnDiskBitmap('/splash.bmp')
logo = displayio.TileGrid(odb, pixel_shader=odb.pixel_shader)
splash.append(logo)

splash.append(icon)
display.show(splash)

time.sleep(1)

# On some boards, we need to give up HID to accomodate MIDI.
# usb_hid.disable()
# usb_midi.enable()


# The switch is the rotary encoder
switch = digitalio.DigitalInOut(board.GP22)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the rotary encoder is not pressed, the drive is writable by circuit python, and does not appear on the computer
# if switch.value:
    #storage.remount("/", False)
    #storage.disable_usb_drive()
    #usb_cdc.disable()
    #pass