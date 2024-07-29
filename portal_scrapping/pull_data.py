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
    c.execute("SELECT temperature, emoji, time, date FROM wp WHERE date = date('now') ORDER BY date ASC")
    data_wp = c.fetchall()
    # print(f'WP prediction for date {date_wp} \n{data_wp}')
    conn.close()

    conn = sqlite3.connect('twoja_pogoda.db')
    c = conn.cursor()
    c.execute("SELECT temperature, emoji, time, date FROM twoja_pogoda WHERE date = date('now') ORDER BY date ASC")
    data_twoja_pogoda = c.fetchall()
    # print(f'\nTwoja Pogoda for date {date_twoja_pogoda} \n{data_twoja_pogoda}')
    conn.close()

    conn = sqlite3.connect('interia.db')
    c = conn.cursor()
    c.execute("SELECT temperature, emoji, time, date FROM interia WHERE date = date('now') ORDER BY date ASC")
    data_interia = c.fetchall()
    # print(f'\nInteria pogoda date {date_interia} \n{data_interia}')
    conn.close()

    return data_interia, data_wp, data_twoja_pogoda

# @scheduler.scheduled_job('cron', minute='0')
def compare_data():
    real_temp, real_emoji, hour = interia_actual_data.scrap_data()
    data_interia, data_wp, data_twoja_pogoda = download_data()

    real_int_temp = int(real_temp)
    hour_index = hour

    interia_temp = data_interia[hour_index][0]
    interia_emoji = data_interia[hour_index][1]

    wp_temp = data_wp[hour_index][0]
    wp_emoji = data_wp[hour_index][1]


    # twoja_pogoda_temp = data_twoja_pogoda[hour_index][0]
    # twoja_pogoda_emoji = data_twoja_pogoda[hour_index][1]

    # print(f'\nPrawdziwa Temperatura: {real_int_temp} \nPogoda: {real_emoji}  \nGodzina: { hour}\n')

    diff_interia_temp = abs(interia_temp - real_int_temp)
    diff_wp_temp = abs(wp_temp - real_int_temp)
    # diff_twoja_pogoda_temp = abs(twoja_pogoda_temp - real_int_temp)

    min_diff = min(diff_interia_temp, diff_wp_temp)#,diff_twoja_pogoda_temp)

    closest_sources = []
    if diff_interia_temp == min_diff:
        closest_sources.append("Interia")
        closest_temperature = interia_temp
    if diff_wp_temp == min_diff:
        closest_sources.append("WP")
        closest_temperature = wp_temp
    # if diff_twoja_pogoda_temp == min_diff:
    #     closest_sources.append("Twoja pogoda")
    #     closest_temperature = twoja_pogoda_temp

    if len(closest_sources) == 1:
        closest_source = closest_sources[0]
        #print(closest_source, '\nróżnica z danymi na żywo:' ,min_diff,'°C')
    else:
        closest_source = ", ".join(closest_sources[:len(closest_sources)])
        #print(closest_source, '\nróżnica z danymi na żywo:' ,min_diff,'°C')
    
    closest_sources_emoji = []
    closest_sources_name_emoji = []
    if real_emoji == interia_emoji:
        closest_sources_emoji.append(interia_emoji)
        closest_sources_name_emoji.append('Interia')
    if real_emoji == wp_emoji:
        closest_sources_emoji.append(wp_emoji)
        closest_sources_name_emoji.append('WP')
    # if real_emoji == twoja_pogoda_emoji:
    #     closest_sources_emoji.append(twoja_pogoda_emoji)
    #     closest_sources_name_emoji.append('Twoja pogoda')

    if len(closest_sources_emoji) == 1 and len(closest_sources_name_emoji) == 1:
        closest_source_emoji = closest_sources_emoji[0]
        closest_source_name_emoji = closest_sources_name_emoji[0]
    elif len(closest_sources_emoji) > 1 and len(closest_sources_name_emoji) > 1:
        closest_source_emoji = ", ".join(closest_sources_emoji)
        closest_source_name_emoji = ", ".join(closest_sources_name_emoji)
    else:
        closest_source_emoji = "❌"
        closest_source_name_emoji = "❌"
        
    conn = sqlite3.connect('general_scoring.db')
    c = conn.cursor()

    c.execute("INSERT INTO general_scoring (real_temperature, real_emoji, the_closest_temp_portal_name, the_closest_emoji_portal_name, portal_emoji, closest_temperature, min_difference) VALUES (?, ?, ?, ?, ?, ?, ?)", (real_int_temp, real_emoji, closest_source, closest_source_name_emoji ,closest_source_emoji, closest_temperature, min_diff))

    conn.commit()
    conn.close

    scoring(closest_source, closest_temperature, min_diff, closest_source_name_emoji, closest_source_emoji)

# create new db with scoring
def scoring(closest_source: str, closest_temperature: int, min_diff: int, closest_source_name_emoji: str, closest_source_emoji: str):
    
    # print(f"Closest source: {closest_source}")
    # print(f"Closest temperature: {closest_temperature}")
    # print(f"Minimum difference: {min_diff}")
    # print(f"Closest source name for emoji: {closest_source_name_emoji}")
    # print(f"Closest source emoji: {closest_source_emoji}")
    
    conn = sqlite3.connect('general_scoring.db')
    c = conn.cursor()

    wp_scoring = 0
    interia_scoring = 0
    twoja_pogoda_scoring = 0
    points = 0
    
    if min_diff == 0:
        points = 10
    elif min_diff == 1:
        points = 8
    elif min_diff == 2:
        points = 6
    elif min_diff == 3:
        points = 4
    elif min_diff == 4:
        points = 2
    elif min_diff == 5:
        points = 1 
    elif min_diff > 5 <= 8:
        points = 0.5
    else:
        points = 0


    sources_list = closest_source.split(', ')
    sources_list_len = len(sources_list)

    for i in range(sources_list_len):
        print(sources_list[i])
        if sources_list[i] == 'WP':
            wp_scoring += points
        elif sources_list[i] == 'Twoja pogoda':
            twoja_pogoda_scoring += points
        elif sources_list[i] == 'Interia':
            interia_scoring += points
        else:
            print("No portal is accurate")
            return

    c.execute("INSERT INTO scoring (wp_scoring, interia_scoring, twoja_pogoda_scoring) VALUES (?, ?, ?)", (wp_scoring, interia_scoring, twoja_pogoda_scoring))

    conn.commit()
    conn.close

    return

scheduler.start()

compare_data()


try:
    while True:
        time.sleep(60)  
except (KeyboardInterrupt):
    scheduler.shutdown()
    print("Scheduler shutdown successfully.")

