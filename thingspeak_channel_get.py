import requests
import json

r = requests.get('https://api.thingspeak.com/channels/723513/feeds.json?api_key=1M45KUAM480PFZWX&results=2')

data = json.loads(r.text)
# Read temperature
print(data['feeds'][0]['field1'])

# Read PIR_1
print(data['feeds'][0]['field2'])

# Read Channel numbers
print(data['channel']['field1'])
print(data['channel']['field2'])

