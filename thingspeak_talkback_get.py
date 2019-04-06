#import RPi.GPIO as GPIO
from urllib.request import urlopen, Request
import requests
import json, time

# variables initialization
PIN = 21
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN, GPIO.OUT)

current_temperature_setting = 20
wating_status = 0

light_1_running = 0
light_1_start = 0
light_1_off = 0

light_1_status = 0


def open_light():
    global light_1_start
    global light_1_status
    light_1_status = 1
    #GPIO.output(PIN, GPIO.HIGH)
    print("light on")
    light_1_start = time.time()

def close_light():
    global light_1_running
    global light_1_start
    global light_1_off
    global light_1_status
    if light_1_status == 0:
        print("light is already closed, do nothing")
    else:
        #GPIO.output(PIN, GPIO.LOW)
        print("light off")
        light_1_status = 0
        light_1_off = time.time()
        light_1_running += (light_1_off - light_1_start)
        light_1_start = 0
        light_1_off = 0
        print('light #1\'s total on time is '  + str(round(light_1_running)) + ' seconds')

def decode_light(command):
    if command == "00":
        close_light()
    elif command == "01":
        open_light()
    else:
        print("invalid light instruction")

def decode_ac(command):
    if command == "000":
        print("air-conditioner off")
    elif command == "010":
        print("air-conditioner on")
    elif command[0] == "1":
        current_temperature_setting = int(command[1:3])
        print("temperature setting is changed to: ", current_temperature_setting)
    else:
        print("invalid AC instruction")

while True:
    try:
        request = Request('https://api.thingspeak.com/talkbacks/31641/commands/execute?api_key=NU6M3B6JB1Q3IR76')
        response = urlopen(request)
        command = response.read().decode()
        '''
        command code:
        [device type(1)][control instruction(2)]
        device type: 0 - lighting system
                     1 - air-conditioner
        000: light off
        001: light on
        1000: air-conditioner off
        1010: air-conditioner on
        11xx: air-conditioner set to xx degrees
        '''
        if not command:
            if wating_status == 0:
                wating_status = 1
                print("waiting for commands...")
                pass
            else:
                pass
        else:
            wating_status = 0
            if command[0] == '0':
                decode_light(command[1:3])

            elif command[0] == '1':
                decode_ac(command[1:4])

            else:
                print("invalid instruction")
    except KeyboardInterrupt:
        #GPIO.output(PIN, GPIO.LOW)
        print("\nExit because user interrupt")
        break
