from urllib.request import urlopen
import requests

baseURL = 'https://api.thingspeak.com/talkbacks/31641/commands'

def post_command(command_string, position):
    instruction = {'api_key': 'NU6M3B6JB1Q3IR76', 'command_string': command_string, 'position': position}
    print("Uploading...")
    thingspeak = requests.post(baseURL, data=instruction)
    print(thingspeak.status_code, thingspeak.reason)
    print("Upload finish")

while True:
    try:
        command_string = str(input('Please input your command: '))
        position = 1
        post_command(command_string, position)
    except KeyboardInterrupt:
        print("\nExit because user interrupt")
        break
