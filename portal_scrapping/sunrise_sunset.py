import requests, datetime
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

def time():
    r = requests.get('https://pogoda.interia.pl/prognoza-szczegolowa-warszawa,cId,36917')
    if r.status_code != 200:
        print("DUPA")
    
    soup = BeautifulSoup(r.content, 'html.parser')

    find_sunrise = soup.find('span', class_='weather-currently-info-sunrise')
    interia_sunrise = find_sunrise.get_text(strip=True)

    find_sunset = soup.find('span', class_='weather-currently-info-sunset')
    interia_sunset = find_sunset.get_text(strip=True)
    
    interia_sunrise_formatted = interia_sunrise[:2]
    interia_sunset_formatted = interia_sunset[:2]

    return interia_sunrise_formatted, interia_sunset_formatted

if __name__ == '__main__':
    time()