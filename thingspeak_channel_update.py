import sys
from time import sleep
#from urllib.request import urlopen
import requests

baseURL = 'https://api.thingspeak.com/update?api_key=T9PJ3W9K7NSQ6AT8&field1=0'

baseURL_temperature_room1 = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field1=0'
baseURL_temperature_PIR1 = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field2=0'
baseURL_temperature_setting_room1 = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field1=0'
baseURL_temperature_setting_room2 = 'https://api.thingspeak.com/update?api_key=LWV7LOPF9QN79QG4&field2=0'

'''
# Update temperature data for room1
temperature = 25
f = requests.get(baseURL_temperature_room1 + str(temperature))
print(f.content)
sleep(1)

# Update PIR_1 data for room1
PIR = 0
f = requests.get(baseURL_temperature_PIR1 + str(PIR))
print(f.content)
sleep(1)
'''

# Update temperature setting for room1
temperature_setting = 25
f = requests.get(baseURL_temperature_setting_room1 + str(temperature_setting))
print(f.content)
sleep(1)

# Update temperature setting for room2
temperature_setting = 25
f = requests.get(baseURL_temperature_setting_room2 + str(temperature_setting))
print(f.content)
sleep(1)

print("over")


