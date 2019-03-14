import RPi.GPIO as GPIO
from urllib.request import urlopen, Request
import requests
#import json, time

PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
while True:
    try:
        request = Request('https://api.thingspeak.com/talkbacks/31641/commands/execute?api_key=NU6M3B6JB1Q3IR76')
        response = urlopen(request)
        command = response.read().decode()
        print(command)
        if command == '1':
            print("light on")
            GPIO.output(PIN, GPIO.HIGH)
        elif command == '0':
            print("light off")
            GPIO.output(PIN, GPIO.LOW)
        else:
            print("no valid instruction")
    except KeyboardInterrupt:
        GPIO.output(PIN, GPIO.LOW)
        print("\nExit because user interrupt")
        break
