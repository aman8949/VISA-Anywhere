import requests

api_address = 'http://api.openweathermap.org/data/2.5/weather?units=metric&appid=d73a909843bf1ed3e1aa9c6364a8841c&q='
city = input("City Name :")

url = api_address + city

json_data = requests.get(url).json()

print(json_data)