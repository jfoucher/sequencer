import board
import digitalio
import storage
import usb_hid, usb_midi
import usb_cdc

# On some boards, we need to give up HID to accomodate MIDI.
# usb_hid.disable()
# usb_midi.enable()


# The switch is the rotary encoder
switch = digitalio.DigitalInOut(board.GP2)

switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# If the rotary encoder is not pressed, the drive is writable by circuit python, and does not appear on the computer
if switch.value:
    storage.remount("/", False)
    storage.disable_usb_drive()
    #usb_cdc.disable()
    #pass