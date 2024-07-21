from bs4 import BeautifulSoup
import requests, sys, re

sys.stdout.reconfigure(encoding='utf-8')

r = requests.get('https://pogoda.wp.pl/pogoda-na-dzis/warszawa/756135')

soup = BeautifulSoup(r.content, 'html.parser')

find_temperatures = soup.find_all('span', class_='temp')

hour_spans = soup.find_all('span', attrs={'data-v-4f287fb8': True})

weather_behavior = soup.find_all('span', class_='desc', attrs={'data-v-4f287fb8': True})


temperature_list = []
hour_list = []
behavior_list = []

time_pattern = re.compile(r'^\d{2}:\d{2}$')

for datas in hour_spans:
    data = datas.get_text(strip=True)
    hour = re.findall(time_pattern, data)
    if hour: 
        hour_list.extend(hour)  
next_2_days_hour = hour_list[46:70]

for temperature in find_temperatures:
    temp = temperature.get_text(strip=True) 
    if temp:
        temperature_list.append(temp)
next_2_days_temp = temperature_list[47:71] 

for behavior in weather_behavior:
    behavior_text = behavior.get_text(strip=True)
    if behavior_text:
        behavior_list.append(behavior_text)
next_2_days_behavior = behavior_list[48:72]


print(next_2_days_behavior[23], next_2_days_hour[23], next_2_days_temp[23])

