#import RPi.GPIO as GPIO
from urllib.request import urlopen, Request
import requests
import json, time

# variables initialization
# Light pin assignment
PIN = 21
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(PIN, GPIO.OUT)

# light 1 related variables
light_1_initialize_flag = 0

current_temperature_setting = 20
waiting_status = 0

light_1_running = 0
light_1_not_running = 0
light_1_start = 0
light_1_off = 0

light_1_time_upload_last = time.time()
light_1_time_upload_now = time.time()

light_1_status = 0

# uploading related variables
baseURL_light_running = 'https://api.thingspeak.com/update?api_key=ZXYPJWBZXNHXGSZB&field1=0'
baseURL_light_off = 'https://api.thingspeak.com/update?api_key=ZXYPJWBZXNHXGSZB&field2=0'


def uploading_light_running_time():
    global light_1_time_upload_now
    global light_1_time_upload_last
    global light_1_running
    global baseURL_light_running
    light_1_time_upload_now = time.time()

    if (light_1_time_upload_now - light_1_time_upload_last) > 15:
        print('uploading')
        f = requests.get(baseURL_light_running + str(light_1_running))
        print(f.content)
        print('uploading succeed')
        light_1_time_upload_last = light_1_time_upload_now
        light_1_running = 0
    else:
        print('not uploading because of the limitation of ThingSpeak')


def uploading_light_off_time():
    global light_1_time_upload_now
    global light_1_time_upload_last
    global light_1_not_running
    global baseURL_light_off
    light_1_time_upload_now = time.time()
    if (light_1_time_upload_now - light_1_time_upload_last) > 15:
        print('uploading')
        f = requests.get(baseURL_light_off + str(light_1_not_running))
        print(f.content)
        print('uploading succeed')
        light_1_time_upload_last = light_1_time_upload_now
        light_1_not_running = 0
    else:
        print('not uploading because of the limitation of ThingSpeak')


def open_light():
    global light_1_start
    global light_1_off
    global light_1_status
    global light_1_not_running
    global light_1_initialize_flag
    if light_1_status == 1:
        print("light is already on, do nothing")
    else:
        light_1_status = 1
        #GPIO.output(PIN, GPIO.HIGH)
        print("light on")
        light_1_start = time.time()
        if light_1_initialize_flag == 0:
            light_1_initialize_flag = 1
            light_1_off = light_1_start
        light_1_not_running += (light_1_start - light_1_off)
        print('light #1\'s total off time is ' + str(round(light_1_not_running)) + ' seconds')
        uploading_light_off_time()


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
        print('light #1\'s total on time is '  + str(round(light_1_running)) + ' seconds')
        uploading_light_running_time()


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
            if waiting_status == 0:
                waiting_status = 1
                print("waiting for commands...")
                pass
            else:
                pass
        else:
            waiting_status = 0
            if command[0] == '0':
                decode_light(command[1:3])

            elif command[0] == '1':
                decode_ac(command[1:4])

            else:
                print("invalid instruction")
    except KeyboardInterrupt:
        print("\nExit because user interrupt")
        if light_1_status == 1:
            #GPIO.output(PIN, GPIO.LOW)
            print("light off")
            light_1_status = 0
            light_1_off = time.time()
            light_1_running += (light_1_off - light_1_start)
        else:
            light_1_not_running += (time.time() - light_1_off)
        uploading_light_running_time()
        uploading_light_off_time()

        '''
        print("Info Summary:")
        print('light #1\'s total on time is ' + str(round(light_1_running)) + ' seconds')
        print('light #1\'s total off time is ' + str(round(light_1_not_running)) + ' seconds')
        '''
        break
