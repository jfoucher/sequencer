from machine import Pin, PWM, Timer
from rotary_irq_rp2 import RotaryIRQ
import neopixel

import time

# 16 step sequencer

# Modes : play, record, ?

# Tapping the rotary encoder button cycles between the modes

# One mode only : 
# if a key is held down, the rotary encoder changes its pitch
# if no key is held down, the rotary encoder changes the tempo
# if the rotary encoder is tapped, it pauses / starts playback
# if the rotary encoder is held down while turned, it sets the last step

# in play mode:
# the rotary encoder changes the tempo
# if rotary encoder is pressed, the keys set the first step
# if rotary encoder is not pressed, the keys set the last step

# in record mode:
# the rotary encoder changes the pitch of the current step
# if rotary encoder is pressed, the keys silence the current step
# if rotary encoder is not pressed, the keys set the current step

RECORD = 0
PLAY = 1

#set default tempo
tempo = 60
#set default sequence
sequence = [0] * 16

# TODO load saved tempo and sequence


# set default mode on boot
mode = RECORD

# set current record step
record_step = 0

# set current play step
play_step = 0

first_step = 0
last_step = 15



rotary_button = Pin(2, Pin.IN, Pin.PULL_UP)

# multiplexed led pins
# the rows will go LOW to turn the row on
lr = [board.GP0, board.GP1, board.GP4, board.GP2]
led_row_pins = []
for l in lr:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = False
    led_row_pins.append(led_pin)
    
lc = [board.GP5, board.GP6, board.GP7, board.GP8]
led_col_pins = []
for l in lc:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = True
    led_col_pins.append(led_pin)


# keyboard matrix
# the rows will go LOW to turn the row on
kr = [board.GP9, board.GP10, board.GP11, board.GP12]
kb_row_pins = []
for l in kr:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.OUTPUT
    led_pin.value = True
    kb_row_pins.append(led_pin)
# the COLS will go low if this key is connected
kc = [board.GP13, board.GP14, board.GP15, board.GP18]
kb_col_pins = []

for l in kc:
    led_pin = digitalio.DigitalInOut(l)
    led_pin.direction = digitalio.Direction.INPUT
    led_pin.pull = digitalio.Pull.UP
    kb_col_pins.append(led_pin)

kb_rows = len(kb_row_pins)

kb_cols = len(kb_col_pins)

current_led = 0
previous_led = 1

debounce_time = 0
pressed_key = 0xFF
old_pressed_key = 0xFF

rotary_button_pressed = 0
debounce_time = 0
debounce_time_rel = 0

last_note_play_time = 0

change_mode = False



def rotary_button_was_pressed():
    global interrupt_flag, debounce_time, rotary_button_pressed
    print(time.ticks_ms()-debounce_time)
    if (time.ticks_ms()-debounce_time) > 50:
        print('clicked')
        rotary_button_pressed = 1
        debounce_time=time.ticks_ms()
        
def rotary_button_released():
    global interrupt_flag, debounce_time_rel, rotary_button_pressed, debounce_time, change_mode
    print(time.ticks_ms()-debounce_time_rel)
    if (time.ticks_ms()-debounce_time_rel) > 50:
        rotary_button_pressed = 0
        debounce_time_rel=time.ticks_ms()
        print('released', debounce_time_rel, debounce_time)
        
    print('released time', debounce_time_rel-debounce_time)
    if (debounce_time_rel-debounce_time) < 1000:
        # pressed and released within 1 second, change mode
        print('changing mode')
        change_mode = True

def rotary_button_interrupt(pin):
    v = pin.value()
    print('pin value', v)
    if(v == 1):
        rotary_button_released()
    else:
        rotary_button_was_pressed()

rotary_button.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=rotary_button_interrupt)


np = neopixel.NeoPixel(Pin(23), 1)

np[0] = (255, 0, 0)

np.write()

def led_display(t):
    # scan the keyboard matrix and turn on the correct LED
    global previous_led
    #print('current_led', current_led)
    # exit if no change
    if (previous_led == current_led):
        return
    # turn on the led that should currently be on according to current_led
    row = current_led // 4
    col = current_led % 4
    #turn everything off
    for pin in led_row_pins:
        pin.off()
    for pin in led_col_pins:
        pin.on()
    # turn our led on
    led_row_pins[row].on()
    led_col_pins[col].off()
    previous_led = current_led
    # current_led+=1
    # if (current_led > last_step):
    #     current_led = first_step
    
led_timer = Timer(period=30, mode=Timer.PERIODIC, callback=led_display)

def scan_matrix(t):
    global pressed_key, debounce_time, old_pressed_key
    
    for r in range(kb_rows):
        # set previous pin high
        kb_row_pins[r-1].on()
        # set current pin LOW
        kb_row_pins[r].off()
        
        # read cols to get pressed key
        for c in range(kb_cols):
            pin = kb_col_pins[c]
            if pin.value() == 0:
                delta = time.ticks_diff(time.ticks_ms(), debounce_time)
                # set pressed key with debounce
                if (delta > 60 and old_pressed_key == r*kb_cols + c):
                    pressed_key = old_pressed_key
                    debounce_time = time.ticks_ms()
                    #print('pressed key', pressed_key)
                    
                old_pressed_key = r*kb_cols + c
                
                
kb_timer = Timer(period=15, mode=Timer.PERIODIC, callback=scan_matrix)

def play_note(midi_note):
    # plays a midi note from 32 to 96
    print("play note", midi_note)

    

# tempo_timer = Timer(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)
# tempo_timer.deinit()



rot = RotaryIRQ(
    pin_num_clk=16, 
    pin_num_dt=17, 
    min_val=0, 
    max_val=15, 
    pull_up=True,
    reverse=False, 
    range_mode=RotaryIRQ.RANGE_WRAP
)

def rotary_changed():
    global sequence, tempo, current_led, record_step
    v = rot.value()
    if mode == RECORD:
        print('v', v)
        current_led = v
        record_step = v
        print('current_led set', current_led)
        sequence[record_step] = v
        
    else:
        tempo = v
        print('tempo set', tempo)
        #tempo_timer.init(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)

rot.add_listener(rotary_changed)


while True:
    if change_mode:
        change_mode = False
        print('current mode', mode)
        if (mode == RECORD):
            mode = PLAY
            play_step = record_step
            rot.set(value=tempo, min_val=0, incr=5,
                max_val=2000, reverse=False, range_mode=RotaryIRQ.RANGE_BOUNDED)
            #tempo_timer.init(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)
            np[0] = (0, 0, 255)
            np.write()
        else: 
            mode = RECORD
            np[0] = (255, 0, 0)
            np.write()
            record_step = play_step
            rot.set(value=play_step, min_val=0, incr=1,
                max_val=15, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)
            
            #tempo_timer.deinit()
            
                
        print('new mode', mode)
        
    delta = time.ticks_diff(time.ticks_ms(), last_note_play_time)
    
    if (mode == PLAY and delta > 60000//tempo):
        last_note_play_time = time.ticks_ms()
        current_led = play_step
        play_note(sequence[play_step])
        play_step += 1
        if (play_step > last_step):
            play_step = first_step
        
        
        
    # if (pressed_key <= len(sequence)):
    #     # do something with the key depending on the mode we're in
    #     if (rotary_button.value() == 0):
    #         # reset interrupt flag
    #         if (rotary_button_pressed == 1):
    #             rotary_button_pressed = 0
    #         if (mode == RECORD):
    #             #Silence this step
    #             sequence[pressed_key] = 0
    #         else:
    #             # Set the first step
    #             first_step = pressed_key
    #     else: # rotary button not pressed
    #         if (mode == RECORD):
    #             current_step = pressed_key
    #             play_note(sequence[pressed_key])
    #         else:
    #             # Set the last step
    #             last_step = pressed_key
                
    #     pressed_key = 0xFF
        
    # else:
    #     if (rotary_button_pressed == 1):
    #         # reset interrupt flag
    #         rotary_button_pressed = 0
    #         # reset rotary encoder value
    #         rot.reset()
    #         # change mode
    #         if (mode == RECORD):
    #             mode = PLAY
    #             current_led = play_step
    #         else:
    #             mode = RECORD
    #             current_led = record
        
    pass