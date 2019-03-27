import requests
import json

r = requests.get('https://api.thingspeak.com/channels/723513/feeds.json?api_key=1M45KUAM480PFZWX&results=2')
r_2 = requests.get('https://api.thingspeak.com/channels/741927/feeds.json?api_key=QZQ9FM7V1MM215R0&results=2')

data = json.loads(r.text)
# Read temperature
print(data['feeds'][0]['field1'])

# Read PIR_1
print(data['feeds'][0]['field2'])

# Read Channel numbers
print(data['channel']['field1'])
print(data['channel']['field2'])

