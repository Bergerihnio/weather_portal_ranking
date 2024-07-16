from bs4 import BeautifulSoup
import requests, sys

sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://pogoda.wp.pl/pogoda-na-dzis/warszawa/756135')

soup = BeautifulSoup(r.content, 'html.parser')

find_temperatures = soup.find_all('span', class_='temp')

find_hours = soup.find_all('span')

hour_spans = soup.find_all('span', attrs={'data-v-4f287fb8': True})
# <span data-v-4f287fb8="">16:00</span>

temperature_list = []
hour_list = []

for hours in hour_spans:
    hour = hours.get_text(strip=True)
    print(hour)

for temperature in find_temperatures:
    temp = temperature.get_text(strip=True) 
    temperature_list.append(temp)

# print(temperature_list[20:25])

