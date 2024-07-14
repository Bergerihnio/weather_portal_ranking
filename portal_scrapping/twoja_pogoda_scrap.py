import requests, json

 # https://www.twojapogoda.pl/prognoza-godzinowa-polska/mazowieckie-warszawa/?page=4

def pull_weather_data():
    response_api = requests.get('https://data.twojapogoda.pl/forecasts/city/hourly/2333/4')

    if response_api.status_code != 200:
        return "ERROR"
    
    data = response_api.text
    parse_json = json.loads(data)
    # print(parse_json)
    exctract_forecast_data(parse_json)

def exctract_forecast_data(parse_json):
    forecast = parse_json['forecasts']

    data = []

    for element in forecast:
        forecast_time = element['name']

        # format time to create "cloudless" case
        f_forecast_time = forecast_time.replace(":00", "")
        int_forecast_time = int(f_forecast_time)
        #####

        forecast_temp = element['temp']
        forecast_behavior = element['sign_desc']

        match forecast_behavior:
            case 'prawie bezchmurnie':
                forecast_behavior = '☁️☀️'
            case 'zachmurzenie umiarkowane':
                forecast_behavior = '☁️'
            case 'bezchmurnie':
                if (int_forecast_time >= 4 and int_forecast_time < 21):
                    forecast_behavior = '☀️' #ADD
                else:
                    forecast_behavior = '🌙'
            case 'zachmurzenie małe':
                forecast_behavior = '☁️'
            case 'burza z deszczem':
                forecast_behavior = '⛈️'
            case 'zachmurzenie małe':
                forecast_behavior = '☁️'
            case 'deszcz':
                forecast_behavior = '🌧️'
            case _:
                forecast_behavior = '❓'
            
        data.append((forecast_time, forecast_temp, forecast_behavior))

    insert_to_db(data)
    print(data)

def insert_to_db(data):
    


if __name__ == '__main__':
    pull_weather_data()