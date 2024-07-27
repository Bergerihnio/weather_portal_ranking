from apscheduler.schedulers.background import BackgroundScheduler
import interia_scrap, wp_scrap, twoja_pogoda_scrap, interia_actual_data
import time, sqlite3

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=2, minute=1)
def wp_pull_data():
    wp_scrap.scrap()

@scheduler.scheduled_job('cron', hour=13, minute=1)
def others_pull_data():
    twoja_pogoda_scrap.scrap()
    interia_scrap.scrap()

def download_data():

    conn = sqlite3.connect('wp.db')
    c = conn.cursor()
    c.execute("SELECT temperature, emoji, time, date FROM wp ORDER BY date ASC LIMIT 24")
    data_wp = c.fetchall()
    date_wp = data_wp[0][3]
    # print(f'WP prediction for date {date_wp} \n{data_wp}')
    conn.close()

    conn = sqlite3.connect('twoja_pogoda.db')
    c = conn.cursor()
    c.execute("SELECT temperature, emoji, time, date FROM twoja_pogoda ORDER BY date ASC LIMIT 24")
    data_twoja_pogoda = c.fetchall()
    date_twoja_pogoda = data_twoja_pogoda[0][3]
    # print(f'\nTwoja Pogoda for date {date_twoja_pogoda} \n{data_twoja_pogoda}')
    conn.close()

    conn = sqlite3.connect('interia.db')
    c = conn.cursor()
    c.execute("SELECT temperature, emoji, time, date FROM interia ORDER BY date ASC LIMIT 24")
    data_interia = c.fetchall()
    date_interia = data_interia[0][3]
    # print(f'\nInteria pogoda date {date_interia} \n{data_interia}')
    conn.close()

    return data_interia, data_wp, data_twoja_pogoda

@scheduler.scheduled_job('cron', minute='0')
def compare_data():
    temp, emoji, hour = interia_actual_data.scrap_data()
    data_interia, data_wp, data_twoja_pogoda = download_data()

    int_temp = int(temp)
    hour_index = hour

    interia_temp = data_interia[hour_index][0]
    interia_emoji = data_interia[hour_index][1]
    interia_date = data_interia[hour_index][2]

    wp_temp = data_wp[hour_index][0]
    wp_emoji = data_wp[hour_index][1]
    wp_date = data_wp[hour_index][2]

    twoja_pogoda_temp = data_twoja_pogoda[hour_index][0]
    twoja_pogoda_emoji = data_twoja_pogoda[hour_index][1]
    twoja_pogoda_date = data_twoja_pogoda[hour_index][2]

    print(f'\nPrawdziwa Temperatura: {int_temp} \nPogoda: {emoji}  \nGodzina: { hour}\n')

    diff_interia_temp = abs(interia_temp - int_temp)
    diff_wp_temp = abs(wp_temp - int_temp)
    diff_twoja_pogoda_temp = abs(twoja_pogoda_temp - int_temp)

    min_diff = min(diff_interia_temp, diff_wp_temp, diff_twoja_pogoda_temp)

    closest_sources = []
    if diff_interia_temp == min_diff:
        closest_sources.append("Interia")
        closest_temperature = interia_temp
    if diff_wp_temp == min_diff:
        closest_sources.append("WP")
        closest_temperature = wp_temp
    if diff_twoja_pogoda_temp == min_diff:
        closest_sources.append("Twoja pogoda")
        closest_temperature = twoja_pogoda_temp

    if len(closest_sources) == 1:
        closest_source = closest_sources[0]
        print(closest_source, '\nróżnica z danymi na żywo:' ,min_diff,'°C')
    else:
        closest_source = ", ".join(closest_sources[:len(closest_sources)])
        print(closest_source, '\nróżnica z danymi na żywo:' ,min_diff,'°C')
    
    conn = sqlite3.connect('general_scoring.db')
    c = conn.cursor()

    c.execute("INSERT INTO general_scoring (temperature, emoji, portal_name, closest_temperature) VALUES (?, ?, ?, ?)", (int_temp, emoji, closest_source, closest_temperature))

    conn.commit()
    conn.close
    
# insert to db: the best portals, time, data, emoji, 
# create new db with scoring

scheduler.start()
# compare_data()

try:
    while True:
        time.sleep(60)  
except (KeyboardInterrupt):
    scheduler.shutdown()
    print("Scheduler shut down successfully.")

