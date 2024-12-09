from flask import Blueprint, render_template, request, session
import requests

weather_bp=Blueprint('weather',__name__)

# Weatherbit API endpoint and key
API_URL = "https://api.weatherbit.io/v2.0/current"
API_KEY = "a5fe95e48d7f4ca2bda3460de183e513"  # 使用你自己的 API 密钥

def get_weather_data(city):
    params = {
        'city': city,
        'key': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

@weather_bp.route('/weather',  methods=['GET', 'POST'])
def weather_query():
    if request.method == 'POST':
        city = request.form['city']
        data = get_weather_data(city)
        if data and data['count'] > 0:
            temperature = data['data'][0]['temp']  # 获取温度
            city_name = data['data'][0]['city_name']
            weather_description = data['data'][0]['weather']['description']
            print(session['username'])
            return render_template('home.html', temperature=temperature, city_name=city_name, weather_description=weather_description, user=session['username'])
        else:
            error_message = "Could not retrieve weather data for the specified city."
            return render_template('home.html', error_message=error_message)
    return render_template('home.html')