from machine import Pin, PWM, Timer
from rotary_irq_rp2 import RotaryIRQ

import time

# 16 step sequencer

# Modes : play, record, ?

# Tapping the rotary encoder button cycles between the modes

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

# set default mode on boot
mode = RECORD

# set current record step
record_step = 0

# set current play step
play_step = 0

first_step = 0
last_step = 15

sequence = [0] * 16

rotary_button = Pin(2, Pin.IN, Pin.PULL_UP)

# multiplexed led pins
# the rows will go LOW to turn the row on
led_row_pins = [Pin(0, Pin.OUT), Pin(1, Pin.OUT), Pin(4, Pin.OUT), Pin(3, Pin.OUT)]
# the COL will go HIGH to turn a specific led ON
led_col_pins = [Pin(5, Pin.OUT), Pin(6, Pin.OUT), Pin(7, Pin.OUT), Pin(8, Pin.OUT), ]

# set rows high
for pin in led_row_pins:
    pin.off()
    
# set cols low
for pin in led_col_pins:
    pin.on()
    
# led_row_pins[0].on()

# led_col_pins[0].off()

# keyboard matrix
# the rows will go LOW to turn the row on
kb_row_pins = [Pin(8, Pin.OUT), Pin(9, Pin.OUT), Pin(10, Pin.OUT), Pin(11, Pin.OUT)]
# the COLS will go low if this key is connected
kb_col_pins = [Pin(12, Pin.IN, Pin.PULL_UP), Pin(13, Pin.IN, Pin.PULL_UP), Pin(14, Pin.IN, Pin.PULL_UP), Pin(15, Pin.IN, Pin.PULL_UP)]

kb_rows = len(kb_row_pins)

kb_cols = len(kb_col_pins)

# set rows high
for pin in kb_row_pins:
    pin.on()

current_led = 0
previous_led = 1

debounce_time = 0
pressed_key = 0xFF
old_pressed_key = 0xFF

rotary_button_pressed = 0
debounce_time = 0

def rotary_button_interrupt(pin):
    global interrupt_flag, debounce_time, rotary_button_pressed
    print(time.ticks_ms()-debounce_time)
    if (time.ticks_ms()-debounce_time) > 500:
        print('clicked')
        rotary_button_pressed = 1
        debounce_time=time.ticks_ms()

rotary_button.irq(trigger=Pin.IRQ_FALLING, handler=rotary_button_interrupt)

def led_display(t):
    # scan the keyboard matrix and turn on the correct LED
    global previous_led
    #print('current_led', current_led)
    # exit if no change
    # if (previous_led == current_led):
    #     return
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

def scan_matrix(t):
    global pressed_key, debounce_time, old_pressed_key
    
    for r in range(kb_rows):
        # set previous pin high
        kb_row_pins[r-1].on()
        # set current pin LOW
        kb_row_pins[r-1].off()
        
        # read cols to get pressed key
        for c in range(kb_cols):
            if pin.value() == 0:
                delta = time.ticks_diff(time.ticks_ms(), debounce_time)
                # set pressed key with debounce
                if (delta > 60 and old_pressed_key == r*kb_cols + c):
                    pressed_key = old_pressed_key
                    debounce_time = time.ticks_ms()
                    
                old_pressed_key = r*kb_cols + c

timer = Timer(period=50, mode=Timer.PERIODIC, callback=led_display)


def play_note(midi_note):
    # plays a midi note from 32 to 96
    print("play note")

    
def play_current_note(t):
    global play_step, current_led, play_step
    play_step = play_step + 1
    if (play_step > last_step):
        play_step = first_step
    current_led = play_step
    
    play_note(sequence[play_step])
    
    print('playing', play_step)
    

tempo_timer = Timer(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)
tempo_timer.deinit()

#kb_timer = Timer(period=15, mode=Timer.PERIODIC, callback=scan_matrix)

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
        sequence[current_step] = v
        
    else:
        tempo = v
        print('tempo set', tempo)
        tempo_timer.init(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)

rot.add_listener(rotary_changed)


while True:
    if rotary_button_pressed == 1:
        rotary_button_pressed = 0
        print('current mode', mode)
        if (mode == RECORD):
            mode = PLAY
            play_step = record_step
            rot.set(value=tempo, min_val=0, incr=5,
                max_val=1000, reverse=False, range_mode=RotaryIRQ.RANGE_BOUNDED)
            tempo_timer.init(period=60000//tempo, mode=Timer.PERIODIC, callback=play_current_note)
        else: 
            mode = RECORD
            rot.set(value=play_step, min_val=0, incr=1,
                max_val=15, reverse=False, range_mode=RotaryIRQ.RANGE_WRAP)
            tempo_timer.deinit()
            
                
        print('new mode', mode)
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