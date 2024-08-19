import requests, datetime
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def scrap_data():
    r = requests.get('https://pogoda.interia.pl/prognoza-szczegolowa-warszawa,cId,36917')
    if r.status_code != 200:
        print("DUPA")
    
    soup = BeautifulSoup(r.content, 'html.parser')
    find_temp = soup.find('div', class_='weather-currently-temp-strict')
    temp = find_temp.get_text(strip=True)
    f_temp = temp.replace("°C", "")

    find_behavior = soup.find('div', class_='weather-currently-icon')
    behavior_title = find_behavior.get('title')

    find_sunrise = soup.find('span', class_='weather-currently-info-sunrise')
    interia_sunrise = find_sunrise.get_text(strip=True)

    find_sunset = soup.find('span', class_='weather-currently-info-sunset')
    interia_sunset = find_sunset.get_text(strip=True)
    
    interia_sunrise_formatted = interia_sunrise[:2]
    interia_sunset_formatted = interia_sunset[:2]

    sunrise_sunset(interia_sunrise_formatted, interia_sunset_formatted)

    time_now = datetime.datetime.now()
    hour = time_now.hour

    match behavior_title:
        case 'Słonecznie':
            behavior_title = '☀️'
        case 'Przeważnie słonecznie':
            behavior_title = '🌤️'
        case 'Częściowo słonecznie':
            behavior_title = '⛅'
        case 'Bezchmurnie':
            if interia_sunrise_formatted <= hour < interia_sunset_formatted:
                behavior_title = '☀️'
            else:
                behavior_title = '🌙'
        case 'Przejściowe zachmurzenie':
            behavior_title = '🌥️'
        case 'Zachmurzenie duże':
            behavior_title = '☁️'
        case 'Zachmurzenie małe':
            if interia_sunrise_formatted <= hour < interia_sunset_formatted:
                behavior_title = '☁️'
            else:
                behavior_title = '🌙'
            behavior_title = '☁️'
        case 'Zachmurzenie umiarkowane':
            behavior_title = '☁️'
        case 'Pochmurno':
            behavior_title = '☁️'
        case 'Deszcz':
            behavior_title = '🌧️'
        case 'Przelotne opady':
            behavior_title = '🌦️'
        case 'Burze z piorunami':
            behavior_title = '⛈️'
        case 'Częściowo słonecznie i burze z piorunami':
            behavior_title = '⛈️'
        case 'Zamglenia':
            behavior_title = '☁️'
        case _:
            behavior_title = '❓'

    return f_temp, behavior_title, hour
    
def sunrise_sunset(interia_sunrise_formatted, interia_sunset_formatted):
    return interia_sunrise_formatted, interia_sunset_formatted

if __name__ == '__main__':
    scrap_data()