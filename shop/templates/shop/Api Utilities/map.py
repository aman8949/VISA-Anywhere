import requests
import urllib.parse

address = 'Lanka, Varanasi, 221005'
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'

response = requests.get(url).json()
print(response[0]['lat'])
print(response[0]['lon'])