from bs4 import BeautifulSoup
import requests, sys, sqlite3

sys.stdout.reconfigure(encoding='utf-8')

def scrap():
    r = requests.get('https://pogoda.interia.pl/pogoda-pojutrze-blonie,cId,1689')

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

    data = merge_data(hours_list, temp_list)

    insert_into_db(data)

def merge_data(hours_list, temp_list):
    data = []

    for score in zip(hours_list, temp_list):
        data.append(score)
    
    return data

def insert_into_db(data):
    conn = sqlite3.connect('interia_temperatures.db')
    c = conn.cursor()

    for element in data:
        time = element[0]
        formatted_time = f'{time}:00'
        temp = element[1]

        c.execute("INSERT INTO interia_temperatures (temperature, time) VALUES (?, ?)",
                (temp, formatted_time))
        conn.commit()
    conn.close()


if __name__ == '__main__':
    scrap()
