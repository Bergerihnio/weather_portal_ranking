from bs4 import BeautifulSoup
import requests, sys, re, sqlite3

sys.stdout.reconfigure(encoding='utf-8')

# Due wp portal architecture we must run this program on 02:00 (at night)

def scrap():
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

    emoji_list = weather_behavior_emoji(next_2_days_behavior, next_2_days_hour)
    
    insert_into_db(emoji_list, next_2_days_temp, next_2_days_hour)

def weather_behavior_emoji(next_2_days_behavior, next_2_days_hour):
    emoji_list = []
    for behavior, hour in zip(next_2_days_behavior, next_2_days_hour):

        int_hour = int(hour[:2])

        match behavior:
            case 'Zachmurzenie małe, pogodnie':
                emoji = '🌤️'
            case 'Zachmurzenie małe, częściowo pogodnie':
                emoji = '⛅'
            case 'Zachmurzenie umiarkowane':
                emoji = '🌥️'
            case 'Prawie bezchmurnie':
                if 4 <= int_hour < 21:
                    emoji = '🌤️'
                else:
                    emoji = '🌙'
            case 'Bezchmurnie, słonecznie':
                if 4 <= int_hour < 21:
                    emoji = '☀️'
                else:
                    emoji = '🌙'
            case 'Zachmurzenie duże':
                emoji = '☁️'
            case 'Pochmurno':
                emoji = '☁️'
            case 'Zachmurzenie umiarkowane, przelotny deszcz':
                emoji = '🌧️'
            case 'Zachmurzenie umiarkowane, deszcz':
                emoji = '🌦️'
            case 'Zachmurzenie umiarkowane, lekki przelotny deszcz':
                emoji = '🌦️'
            case 'Zachmurzenie małe, pogodnie, ulewa':
                emoji = '🌦️'
            case 'Zachmurzenie umiarkowane, ulewa':
                emoji = '🌦️'
            case 'Zachmurzenie umiarkowane, burze':
                emoji = '⛈️'
            case 'Zachmurzenie duże i burze z piorunami':
                emoji = '⛈️'
            case 'Częściowo słonecznie i burze z piorunami':
                emoji = '⛈️'
            case _:
                emoji = '❓'
        emoji_list.append(emoji)

    return emoji_list

def insert_into_db(emoji_list, next_2_days_temp, next_2_days_hour):

    conn = sqlite3.connect('wp.db')
    c = conn.cursor()

    for emoji, temp, time in zip(emoji_list, next_2_days_temp, next_2_days_hour):
        formatted_temp = temp.replace("°C", "")
        
        c.execute("INSERT INTO wp (temperature, time, emoji) VALUES (?, ?, ?)",
                  (formatted_temp, time, emoji))
        conn.commit()
    conn.close()


if __name__ == '__main__':
    scrap()

