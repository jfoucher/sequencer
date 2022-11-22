import board
#import neopixel
import keypad
import time
import digitalio
import rotaryio
import neopixel
import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn
from adafruit_midi.pitch_bend import PitchBend
from adafruit_midi.timing_clock import TimingClock
from adafruit_midi.program_change import ProgramChange
from adafruit_midi.mtc_quarter_frame import MtcQuarterFrame
from adafruit_midi.control_change import ControlChange

# 16 step sequencer

# if a key is held down, the rotary encoder changes its pitch
# if no key is held down, the rotary encoder changes the tempo
# if the rotary encoder is tapped, it pauses / starts playback
# if the rotary encoder is held down while turned, it sets the last step


#set default tempo
tempo = 600
#set default sequence
sequence = [52, 55, 57, 55, 62,60, 62, 64, 0, 0, 0, 0, 0, 0, 0, 0]

active = [True] * 16

# TODO load saved tempo and sequence
midi = adafruit_midi.MIDI(
    midi_in=usb_midi.ports[0],
    midi_out=usb_midi.ports[1],
    out_channel=0
)

pixels = neopixel.NeoPixel(
    board.GP23, 1, brightness=1, auto_write=False
)

pixels.fill((255, 0, 0))
pixels.show()

# set default mode on boot
playing = False

# set current play step
play_step = 0

first_step = 0
last_step = 7

def load_data():
    global tempo, last_step, sequence, active
    with open("/params", "rb") as fp:
        d = fp.read(128)
        if len(d):
            tempo = d[0] | d[1] << 8
            last_step = d[2]
            if len(d) > 19:
                sequence = [d[3], d[4], d[5], d[6], d[7], d[8], d[9], d[10], d[11], d[12], d[13], d[14], d[15], d[16], d[17], d[18]]
            if len(d) > 35:
                active = [d[19], d[20], d[21], d[22], d[23], d[24], d[25], d[26], d[27], d[28], d[129], d[30], d[31], d[32], d[33], d[34]]

def save_data():
    data = [tempo & 0xFF, tempo >> 8, last_step] + sequence + active 
    try:
        with open("/params", "wb") as fp:
            fp.write(bytearray(data))
        return 1
    except:
        print('Could not save data')
        return 0
        
load_data()
#rotary_button = Pin(2, Pin.IN, Pin.PULL_UP)

# multiplexed led pins
# the rows will go LOW to turn the row on
# lr = [board.GP0, board.GP1, board.GP4, board.GP3]
lr = [board.GP3, board.GP4, board.GP1, board.GP0]
led_row_pins = []
for l in lr:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = False
    led_row_pins.append(led_pin)
    
# lc = [board.GP5, board.GP6, board.GP7, board.GP8]
lc = [board.GP8, board.GP7, board.GP6, board.GP5]
led_col_pins = []
for l in lc:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = True
    led_col_pins.append(led_pin)


# keyboard matrix
# the rows will go LOW to turn the row on
keys = keypad.KeyMatrix(
    row_pins=(board.GP12, board.GP11, board.GP10, board.GP9),
    column_pins=(board.GP18, board.GP15, board.GP14, board.GP13),
    columns_to_anodes=True,
)



current_led = 0
previous_led = 1

debounce_time = 0
pressed_key = False

autosave_interval = 30
last_autosave_time = time.monotonic()

rotary_button_pressed = 0
debounce_time = 0
debounce_time_rel = 0

last_note_play_time = 0

change_mode = False

led_display_delay = 0.005

last_step_display_time = 0
last_pressed_key_display_time = 0

rotary_button = keypad.Keys((board.GP2,), value_when_pressed=False, pull=True)
rotary_pressed_time = 0
rotary_release_time = 0
rotary_pressed = False

encoder = rotaryio.IncrementalEncoder(board.GP17, board.GP16)
encoder.position = tempo//5

last_save_data = 0

def play_note(midi_note):
    # plays a midi note from 32 to 96
    if (midi_note < 0x7F):
        message = NoteOn(midi_note)
        midi.send(message)
        
    
    
def led_display(led):
    # scan the keyboard matrix and turn on the correct LED
    global previous_led
    # exit if no change
    # if (previous_led == led):
    #     return
    
    #turn everything off
    for pin in led_row_pins:
        pin.value = False
    for pin in led_col_pins:
        pin.value = True
    # turn our led on
    if (led < 16 and led >= 0):
        # turn on the led that should currently be on according to current_led
        row = led // 4
        col = led % 4
        led_row_pins[row].value = True
        led_col_pins[col].value = False
    previous_led = led
    
last_note_off_time = 30/tempo

while True:
    t = time.monotonic()
    delta = t - last_note_play_time
    delta_off = t - last_note_off_time

    if (playing and tempo > 0 and delta > 60/tempo):
        last_note_play_time = t
        current_led = play_step
        if (active[play_step]):
            play_note(sequence[play_step])
        play_step += 1
        if (play_step > last_step):
            play_step = first_step
    elif(playing and tempo > 0 and delta > 30/tempo and delta_off >= 60/tempo):
        last_note_off_time = t
        print('play_step', play_step)
        
        ps = play_step - 1
        if ps < 0:
            ps = last_step
        print('ps', ps)
            
        if (active[ps]):
            message = NoteOff(sequence[ps])
            midi.send(message)
        
    event = rotary_button.events.get()
    # event will be None if nothing has happened.
    if event:
        if (event.pressed):
            rotary_pressed_time = t
        else: 
            rotary_release_time = t
            last_save_data = 0
            if rotary_pressed:
                rotary_pressed = False
                if (pressed_key):
                    encoder.position = sequence[pressed_key]
                else:
                    encoder.position = tempo // 5
            
        if (rotary_pressed_time < rotary_release_time and rotary_release_time - rotary_pressed_time < 0.5):
            if (isinstance(pressed_key, int)):
                active[pressed_key] = not active[pressed_key]
                print('Toggling note', pressed_key, active[pressed_key])
            else:
                print('changing mode')
                playing = not playing
                if (playing):
                    pixels.fill((0, 255, 0))
                else:
                    pixels.fill((255, 0, 0))
                pixels.show()
        
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        if event.pressed:
            pressed_key = event.key_number
            encoder.position = sequence[pressed_key]
        else:
            pressed_key = False
            encoder.position = tempo // 5
            
    
    if (rotary_pressed_time > rotary_release_time and t - rotary_pressed_time > 1 and encoder.position == last_step and playing == False and last_save_data == 0):
        if save_data():
            for l in range(6):
                led_display(l)
                time.sleep(0.2)
        else:
            for l in range(6):
                led_display(l%2)
                time.sleep(0.2)
            
        last_save_data = 1
        
    if (rotary_pressed_time > rotary_release_time and t - rotary_pressed_time > 0.5 and rotary_pressed == False):
        # rotary encoder is held down
        rotary_pressed = True
        # set encoder position to last step
        
        encoder.position = last_step
    
    if (encoder.position < 0):
        encoder.position = 0
        
    if (encoder.position > 0 and pressed_key == False and not isinstance(pressed_key, int) and tempo != (encoder.position * 5) and rotary_pressed == False):
        tempo = encoder.position * 5
    elif (isinstance(pressed_key, int) and rotary_pressed == False):
        if not playing and sequence[pressed_key] != encoder.position:
            play_note(encoder.position)
        sequence[pressed_key] = encoder.position
        
    elif (rotary_pressed == True):
        # turning while pressing : set last step
        last_step = encoder.position
        if (last_step > 15):
            last_step = 0
        if last_step < 0:
            last_step = 0
            
    if (t - last_autosave_time > autosave_interval and not playing):
        #save_data()
        last_autosave_time = t
        
        
    # Display current step led
    if (t - last_step_display_time > led_display_delay):
        if (active[current_led]):
            led_display(current_led)
        else:
            led_display(-1)
        last_step_display_time = t
    #display pressed key LED
    if (t - last_pressed_key_display_time > led_display_delay and isinstance(pressed_key, int)):
        led_display(pressed_key)
        last_pressed_key_display_time = t
    # display step change LED
    if (t - last_pressed_key_display_time > led_display_delay and rotary_pressed == True):
        led_display(last_step)
        last_pressed_key_display_time = t
