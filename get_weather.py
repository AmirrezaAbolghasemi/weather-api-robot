import requests

api_key = "<API-KEY>"

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        main = data['main']
        weather = data['weather'][0]
        wind = data['wind']

        print(f"status {city}:")
        print(f"tempreture: {main['temp']}°C")
        print(f"description : {weather['description']}")
        print(f"humidity: {main['humidity']}%")
        print(f"speed: {wind['speed']} ")
    else:
        print("Not found your city ...")
