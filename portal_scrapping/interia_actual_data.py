import requests, datetime
from bs4 import BeautifulSoup
import sys
import sunrise_sunset

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

    interia_sunrise, interia_sunset = sunrise_sunset.time()

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
            if interia_sunrise <= hour < interia_sunset:
                behavior_title = '☀️'
            else:
                behavior_title = '🌙'
        case 'Przejściowe zachmurzenie':
            behavior_title = '🌥️'
        case 'Zachmurzenie duże':
            behavior_title = '☁️'
        case 'Zachmurzenie małe':
            if interia_sunrise <= hour < interia_sunset:
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
    

if __name__ == '__main__':
    scrap_data()