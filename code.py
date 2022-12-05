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
import displayio
import adafruit_displayio_ssd1306
import adafruit_imageload
import adafruit_mcp4725
from adafruit_display_text import label
import busio
import terminalio

notes = [
    "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"
]

def midi_note_name(midi_note):
    n = midi_note - 24
    octave = n // 12
    note = notes[n%12]
    return note+str(octave)
    

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

uart = busio.UART(tx=board.GP16, rx=board.GP17, baudrate=31250, timeout=0.001)

serial_midi = adafruit_midi.MIDI(midi_in=uart, midi_out=uart)

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

# Gate signal
gate_pin = digitalio.DigitalInOut(board.GP18)
gate_pin.direction = digitalio.Direction.OUTPUT
gate_pin.value = False

def midi_to_cv(midi_note):
    n = midi_note - 36
    if (n > 60):
        n = 60
    if (n < 0):
        n = 0
    dc = pwms[n]
    if dc > 65535:
        dc = 65535
    if dc < 0:
        dc = 0
    return dc
    
pwms = []
note_pwm = 0
ratio = 65535 / 5
# This creates a pwm value for each note
for pitch in range(61):
    voltage = pitch / 12
    pwm = voltage * ratio
    pwms.append(int(pwm))


displayio.release_displays()

# Use for I2C
i2c = busio.I2C(scl=board.GP21, sda=board.GP20, frequency=300000)


dac = adafruit_mcp4725.MCP4725(i2c, address=0x60)

display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 32


display = adafruit_displayio_ssd1306.SSD1306(display_bus, width=WIDTH, height=HEIGHT, rotation=180)


sprite_sheet, palette = adafruit_imageload.load("spritesheet.bmp",
bitmap=displayio.Bitmap, palette=displayio.Palette
)

sprite = displayio.TileGrid(sprite_sheet, pixel_shader=palette,
                            width = 1,
                            height = 1,
                            tile_width = 11,
                            tile_height = 11)

# Create a Group to hold the sprite
icon = displayio.Group(scale=1)

# Add the sprite to the Group
icon.append(sprite)

# Add the Group to the Display


# Set sprite location
icon.x = 117
icon.y = 0

# Make the display context
splash = displayio.Group()
screen = displayio.Group()

screen.append(splash)

screen.append(icon)

display.show(screen)

# Draw the tempo
tempo_text = label.Label(
    terminalio.FONT, text=" " * 4, color=0xFFFFFF, x=0, y=6, scale=2
)
tempo_text.text = str(tempo)
splash.append(tempo_text)

legend = label.Label(
    terminalio.FONT, text="Tempo", color=0xFFFFFF, x=0, y=25, scale=1
)
splash.append(legend)

note_legend = label.Label(
    terminalio.FONT, text="Note", color=0xFFFFFF, x=60, y=25, scale=1
)
splash.append(note_legend)

#Draw the note
note_text = label.Label(
    terminalio.FONT, text=" " * 3, color=0xFFFFFF, x=60, y=6, scale=2
)
note_text.text = midi_note_name(sequence[0])

splash.append(note_text)
display.refresh()



# multiplexed led pins
# the rows will go LOW to turn the row on
# lr = [board.GP0, board.GP1, board.GP4, board.GP3]
lr = [board.GP1, board.GP0, board.GP3, board.GP2, ]
led_row_pins = []
for l in lr:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = False
    led_row_pins.append(led_pin)
    
# lc = [board.GP5, board.GP6, board.GP7, board.GP8]
lc = [board.GP7, board.GP6, board.GP5, board.GP4]
led_col_pins = []
for l in lc:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = True
    led_col_pins.append(led_pin)


# keyboard matrix
# the rows will go LOW to turn the row on
keys = keypad.KeyMatrix(
    row_pins=(board.GP9, board.GP8, board.GP11, board.GP10),
    column_pins=(board.GP15, board.GP14, board.GP13, board.GP12,),
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

rotary_button = keypad.Keys((board.GP22,), value_when_pressed=False, pull=True)
rotary_pressed_time = 0
rotary_release_time = 0
rotary_pressed = False

encoder = rotaryio.IncrementalEncoder(board.GP26, board.GP27)
encoder.position = tempo//5

last_save_data = 0
last_note_off_time = 30/tempo
recording = False
rotary_tapped_time = 0

tt = tempo

def note_on(midi_note):
    # plays a midi note from 32 to 96
    if (midi_note < 0x7F and midi_note >= 0):
        message = NoteOn(midi_note)
        midi.send(message)
        serial_midi.send(message)
        
        gate_pin.value = True
        try: 
            dac.value = midi_to_cv(midi_note)
        except Exception as e: 
            pass
            # print(e)
        
def note_off(midi_note):
    # plays a midi note from 32 to 96
    if (midi_note < 0x7F and midi_note >= 0):
        message = NoteOff(midi_note)
        midi.send(message)
        serial_midi.send(message)
        gate_pin.value = False
    
    
def led_display(led):
    # scan the keyboard matrix and turn on the correct LED
    global previous_led
    # exit if no change
    if (previous_led == led):
        return
    
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
    
record_step = 0

new_last_step = last_step
set_last_step = False

while True:
    t = time.monotonic()
    delta = t - last_note_play_time
    delta_off = t - last_note_off_time
    
    if set_last_step and play_step == 0:
        stride = 1 if last_step < new_last_step else -1
        print("last_step, new_last_step, stride", last_step, new_last_step, stride)
        for n in range(last_step, new_last_step, stride):
            print(n)
            note_off(sequence[n])
            
        last_step = new_last_step
        set_last_step = False
                
    if (playing and tempo > 0 and delta > 60/tempo):
        # send note on and increment current step
        last_note_play_time = t
        current_led = play_step
        if (active[play_step]):
            note_on(sequence[play_step])
        play_step += 1
        if (play_step > last_step):
            play_step = first_step
    elif(playing and tempo > 0 and delta > 30/tempo and delta_off > 60/tempo):
        # send note off halfway to the next note
        last_note_off_time = t
        
        ps = play_step - 1
        if ps < 0:
            ps = last_step
            
        if (active[ps]):
            note_off(sequence[ps])
            

            
    if recording:
        # Listen to USB midi message and set current note 
        message = midi.receive()
        #if last_recorded_step != play_step:
        if (isinstance(message, NoteOn)):
            sequence[record_step] = message.note
            print('set step ', record_step, ' to ', message.note)
            note_on(message.note)
            note_text.text = midi_note_name(message.note)
            time.sleep(0.1)
            note_off(message.note)
            record_step += 1
            if (record_step > last_step):
                record_step = first_step
                #last_recorded_step = play_step
            current_led = record_step
            
        # Listen to serial midi message and set current note 
        message = serial_midi.receive()
        #if last_recorded_step != play_step:
        if (isinstance(message, NoteOn)):
            sequence[record_step] = message.note
            print('set step ', record_step, ' to ', message.note)
            note_on(message.note)
            note_text.text = midi_note_name(message.note)
            time.sleep(0.1)
            note_off(message.note)

            record_step += 1
            if (record_step > last_step):
                record_step = first_step
                #last_recorded_step = play_step
            current_led = record_step
        
    event = rotary_button.events.get()
    # event will be None if nothing has happened.
    if event:
        if (event.pressed):
            rotary_pressed_time = t
            rotary_pressed = True
            # set encoder position to last step
            
            encoder.position = last_step
            new_last_step = last_step
        else: 
            rotary_release_time = t
            last_save_data = 0
            if rotary_pressed:
                # release rotary button
                rotary_pressed = False
                if (pressed_key):
                    encoder.position = sequence[pressed_key]
                else:
                    set_last_step = True
                    encoder.position = tempo // 5
                    
        
            
        if (rotary_pressed_time < rotary_release_time and rotary_release_time - rotary_pressed_time < 0.5):
            if (isinstance(pressed_key, int)):
                active[pressed_key] = not active[pressed_key]
                # when a key is pressed and the rotary encoder is tapped,
                # the step is disabled
            else:
                recording = False
                # If no key is pressed, start playing or pause playing
                playing = not playing
                if (playing):
                    pixels.fill((0, 255, 0))
                    sprite[0] = 1
                else:
                    pixels.fill((255, 0, 0))
                    sprite[0] = 0
                    # if pausing, send note off midi for current note
                    note_off(sequence[current_led])
                
                # if rotary button was tapped a short time ago, set record mode
                if (t - rotary_tapped_time < 0.5):
                    note_off(sequence[current_led])
                    sprite[0] = 2
                    recording = True
                    playing = False
                    pixels.fill((255, 0, 255))
                    record_step = 0
                    current_led = 0
                    # if pausing, send note off midi for current note
                    
                    
                pixels.show()
                rotary_tapped_time = t


                
                
            
        
    event = keys.events.get()
    # event will be None if nothing has happened.
    if event:
        if event.pressed:
            pressed_key = event.key_number
            encoder.position = sequence[pressed_key]
            note_text.text = midi_note_name(sequence[pressed_key])
            if (recording):
                record_step = pressed_key
                current_led = record_step
        else:
            note_text.text = " "
            pressed_key = False
            encoder.position = tempo // 5
    
    if (rotary_pressed_time > rotary_release_time and t - rotary_pressed_time > 1 and encoder.position == last_step and playing == False and last_save_data == 0):
        # if playback is paused and the rotary encoder is held, save data
        if save_data():
            for l in range(6):
                led_display(l%2)
                time.sleep(0.2)
        else:
            for l in range(6):
                led_display(0)
                time.sleep(0.1)
                led_display(-1)
                time.sleep(0.1)
            
        last_save_data = 1
        

    
    if (encoder.position < 0):
        encoder.position = 0
        
    if (encoder.position > 0 and pressed_key == False and not isinstance(pressed_key, int) and tempo != (encoder.position * 5) and rotary_pressed == False):
        tempo = encoder.position * 5
        if (tempo <= 0):
            tempo = 1
            encoder.position = tempo // 5
        if (tempo > 3000):
            tempo = 3000
            encoder.position = tempo // 5
            
        
    elif (isinstance(pressed_key, int) and rotary_pressed == False and sequence[pressed_key] != encoder.position):
        if not playing:
            note_on(encoder.position)
            note_off(encoder.position)
        else:
            note_off(sequence[pressed_key])
        sequence[pressed_key] = encoder.position
        note_text.text = midi_note_name(encoder.position)
        
        
    elif (rotary_pressed == True):
        # turning while pressing : set last step
        if new_last_step != encoder.position:
            # turn off last step in case it was on
            if encoder.position < new_last_step:
                note_off(sequence[new_last_step])
            new_last_step = encoder.position
            if (new_last_step > 15):
                new_last_step = 15
            if new_last_step < 0:
                new_last_step = 0
            
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
    if (t - last_pressed_key_display_time > led_display_delay and rotary_pressed == True and t - rotary_pressed_time > 0.2):
        led_display(new_last_step)
        last_pressed_key_display_time = t
        
    time_spent = time.monotonic() - t
        
    if (time_spent < 1/tempo and tt != tempo):
        tempo_text.text = str(tempo)
        print("tempo", tempo, (time.monotonic() - t)*1000, 30000/tempo)
        tt = tempo
