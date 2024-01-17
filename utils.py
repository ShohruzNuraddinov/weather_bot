import requests

from datetime import datetime, timedelta
import json

# Replace 'YOUR_API_KEY' with your actual OpenWeatherMap API key
api_key = 'be06bd2df269c773a1472ea7e9421c0a'

# Replace 'YOUR_CITY' and 'YOUR_COUNTRY_CODE' with the city and country code you want to get the weather for

# Construct the API URL


def one_week(country_name: str):
    # base_url = 'https://api.openweathermap.org/data/2.5/forecast'
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={country_name}&lang=en&appid=be06bd2df269c773a1472ea7e9421c0a"

    # try:
    # Send a GET request to the OpenWeatherMap API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        text = ''

        # Extract and print the weather information for the next 7 days
        for data in data['list']:
            date = data['dt_txt']
            temperature = data['main']['temp']

            text += f"Sana: <b>{date}</b>\n\tTemp: <b>{int(temperature-273.15)}°C</b>\n\t\tHolat: <b>{data['weather'][0]['main']}</b>\n\n"

        return text


def today_weather(country_name: str):
    # Calculate the date for tomorrow
    today = datetime.now()
    date_str = today.strftime('%Y-%m-%d')

    # Construct the API URL
    base_url = 'https://api.openweathermap.org/data/2.5/weather'
    url = f"{base_url}?q={country_name}&appid={api_key}"

    # Send a GET request to the OpenWeatherMap API
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        temp = int(data['main']['temp'] - 273.15)
        temp_max = int(data['main']['temp_max'] - 273.15)
        temp_min = int(data['main']['temp_min'] - 273.15)
        weather = data['weather'][0]['main']
        return f"Holat: <b>{weather}</b>\nTemp: <b>{temp}°C</b>\nMax Temp: <b>{temp_max}°C</b>\nMin Temp: <b>{temp_min}°C</b>", data['weather'][0]['icon']


def get_district_data(district_id):
    with open('utils/districts.json', 'r') as f:
        json_data = json.load(f)

    for district in json_data:
        if district['id'] == district_id:
            return district
