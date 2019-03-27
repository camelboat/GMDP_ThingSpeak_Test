#import RPi.GPIO as GPIO
from urllib.request import urlopen, Request
import requests
import json, time

PIN = 21
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN, GPIO.OUT)

current_temperature_setting = 20
wating_status = 0

def decode_light(command):
    if command == "00":
        print("light off")
        #GPIO.output(PIN, GPIO.LOW)
    elif command == "01":
        print("light on")
        #GPIO.output(PIN, GPIO.HIGH)
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
        #if command == '1':
        #    print("light on")
        #    #GPIO.output(PIN, GPIO.HIGH)
        #elif command == '0':
        #    print("light off")
        #    #GPIO.output(PIN, GPIO.LOW)

            else:
                print("invalid instruction")
    except KeyboardInterrupt:
        #GPIO.output(PIN, GPIO.LOW)
        print("\nExit because user interrupt")
        break
