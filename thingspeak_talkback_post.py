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
        command_string = str(input('''Please input your command:\n1. open the light\n2. close the light\n3. open the air-conditioner\n4. close the air-conditioner\nor input 11xx, where xx is the air-conditioner degree\n'''))
        if command_string == '1':
            command_string = '0010'
        elif command_string == '2':
            command_string = '0000'
        elif command_string == '3':
            command_string = '1010'
        elif command_string == '4':
            command_string = '1000'
        position = 1
        post_command(command_string, position)
    except KeyboardInterrupt:
        print("\nExit because user interrupt")
        break
