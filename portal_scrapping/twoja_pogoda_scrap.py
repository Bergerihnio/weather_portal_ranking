import requests
import json
import sqlite3
from datetime import datetime, timedelta

# Due twojapogoda portal architecture we must run this program beetween 1-9 PM
 
# https://www.twojapogoda.pl/prognoza-godzinowa-polska/mazowieckie-warszawa/?page=3, 
link_1 = 'https://data.twojapogoda.pl/forecasts/city/hourly/2333/3'
# DONE https://www.twojapogoda.pl/prognoza-godzinowa-polska/mazowieckie-warszawa/?page=4 , 
link_2 = 'https://data.twojapogoda.pl/forecasts/city/hourly/2333/4'
# https://www.twojapogoda.pl/prognoza-godzinowa-polska/mazowieckie-warszawa/?page=5 , 
link_3 = 'https://data.twojapogoda.pl/forecasts/city/hourly/2333/5'


date = datetime.now()
future_date = date + timedelta(days=2)
next_2days_date = future_date.strftime("%d.%m.%Y")


def pull_weather_data(link):
    response_api = requests.get(link)

    if response_api.status_code != 200:
        return "ERROR"

    data = response_api.text
    parse_json = json.loads(data)
        
    exctract_forecast_data(parse_json)


def exctract_forecast_data(parse_json):
    forecast = parse_json['forecasts']

    data = []

    for element in forecast:
        forecast_time = element['name']

        # format time to create "cloudless" case
        f_forecast_time = forecast_time.replace(":00", "")
        int_forecast_time = int(f_forecast_time)

        forecast_temp = element['temp']
        forecast_behavior = element['sign_desc']

        forecast_mutable = element['date']
        forecast_split = forecast_mutable.split(',')
        forecast_date_text = forecast_split[1]
        forecast_date = forecast_date_text.replace(" ", "", 1)

        match forecast_behavior:
            case 'prawie bezchmurnie':
                forecast_behavior = '🌤️' 
            case 'zachmurzenie umiarkowane':
                forecast_behavior = '⛅'
            case 'bezchmurnie':
                if (int_forecast_time >= 4) and (int_forecast_time < 21):
                    forecast_behavior = '☀️'
                else:
                    forecast_behavior = '🌙'
            case 'zachmurzenie małe':
                forecast_behavior = '⛅'
            case 'burza z deszczem':
                forecast_behavior = '⛈️'
            case 'deszcz':
                forecast_behavior = '🌧️'
            case 'pochmurno':
                forecast_behavior = '☁️'
            case _:
                forecast_behavior = '❓'
        if forecast_date == next_2days_date:
            data.append((forecast_time, forecast_temp, forecast_behavior))

    insert_to_db(data)


def insert_to_db(data):
    conn = sqlite3.connect('forecast_data.db')
    c = conn.cursor()

    for element in data:
        time = element[0]
        temp = element[1]
        emoji = element[2]

        c.execute(
            "INSERT INTO twoja_pogoda (temperature, time, emoji) VALUES (?, ?, ?)", (temp, time, emoji))
        conn.commit()
    conn.close

def scrap():
    pull_weather_data(link_1) # last 4, 8 to remove from 12
    pull_weather_data(link_2) # all data
    pull_weather_data(link_3) # first 3 from 12
    
if __name__ == '__main__':
    scrap()