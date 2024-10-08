from bs4 import BeautifulSoup
import requests
import sys
import sqlite3
import sunrise_sunset

sys.stdout.reconfigure(encoding='utf-8')


def scrap():
    r = requests.get(
        'https://pogoda.interia.pl/pogoda-pojutrze-warszawa,cId,36917')

    if r.status_code != 200:
        print(r.status_code)
        return

    soup = BeautifulSoup(r.content, 'html.parser')

    find_hours = soup.find_all('span', class_='hour')
    hours_list = []

    for hours in find_hours:
        hour = hours.get_text(strip=True)
        hours_list.append(hour)

    find_temp = soup.find_all('span', class_='forecast-temp')
    temp_list = []

    for temps in find_temp:
        temp = temps.get_text(strip=True)
        formatted_temp = temp.replace("°C", "")
        temp_list.append(formatted_temp)

    list_behave = scrap_behavior(soup, hours_list)

    data = merge_data(hours_list, temp_list, list_behave)

    insert_into_db(data)


def merge_data(hours_list, temp_list, list_behave):
    data = []

    for score in zip(hours_list, temp_list, list_behave):
        data.append(score)

    return data


def scrap_behavior(soup, hours_list):

    find_behave = soup.find_all('span', class_='forecast-icon')

    list_behave = []

    sunrise_time, sunset_time = sunrise_sunset.time()

    for index, title in enumerate(find_behave):
        title_text = title.get('title')
        hour_str = hours_list[index]
        int_hour = int(hour_str)

        match title_text:
            case 'Słonecznie':
                title_text = '☀️'
            case 'Przeważnie słonecznie':
                title_text = '🌤️'
            case 'Częściowo słonecznie':
                title_text = '⛅'
            case 'Przejściowe zachmurzenie':
                title_text = '🌥️'
            case 'Bezchmurnie':
                if (sunrise_time >= 4) and (sunset_time < 21):
                    title_text = '☀️'
                else:
                    title_text = '🌙'
            case 'Zachmurzenie duże':
                title_text = '☁️'
            case 'Zachmurzenie małe':
                title_text = '⛅'
            case 'Zachmurzenie umiarkowane':
                title_text = '⛅'
            case 'Pochmurno':
                title_text = '☁️'
            case 'Deszcz':
                title_text = '🌧️'
            case 'Przelotne opady':
                title_text = '🌦️'
            case 'Burze z piorunami':
                title_text = '⛈️'
            case 'Zachmurzenie duże i burze z piorunami':
                title_text = '⛈️'
            case 'Częściowo słonecznie i burze z piorunami':
                title_text = '⛈️'
            case 'Zamglenia':
                title_text = '☁️'
            case _:
                title_text = '❓'

        list_behave.append(title_text)

    return list_behave


def insert_into_db(data):
    conn = sqlite3.connect('forecast_data.db')
    c = conn.cursor()

    for element in data:
        time = element[0]
        int_time = int(time)
        if int_time < 10:
            int_time = f'0{int_time}'

        formatted_time = f'{int_time}:00'
        temp = element[1]
        emoji = element[2]

        c.execute("INSERT INTO interia (temperature, time, emoji) VALUES (?, ?, ?)",
                  (temp, formatted_time, emoji))
        conn.commit()
    conn.close()


if __name__ == '__main__':
    scrap()
