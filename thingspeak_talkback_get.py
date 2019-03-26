#import RPi.GPIO as GPIO
from urllib.request import urlopen, Request
import requests
import json, time

PIN = 21
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN, GPIO.OUT)

current_temperature_setting = 20

def decode_light(command):
    print(command)
    if command == "00":
        print("light off")
    elif command == "01":
        print("light on")
    else:
        print("invalid light instruction")

def decode_ac(command):
    if command == "00":
        print("air-conditioner off")
    elif command == "01":
        print("air-conditioner on")
    elif command == "10":
        current_temperature_setting -= 1
        print("temperature setting is changed to: ", current_temperature_setting)
    elif command == "11":
        current_temperature_setting += 1
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
        100: air-conditioner off
        101: air-conditioner on
        110: air-conditioner decrease 1 degree
        111: air-conditioner increase 1 degree
        '''
        print(command)
        if not command:
            print("no instruction")
        elif command[0] == '0':
            decode_light(command[1:3])

        elif command[0] == '1':
            decode_ac(command[1:3])
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
