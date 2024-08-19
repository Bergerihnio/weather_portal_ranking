from apscheduler.schedulers.background import BackgroundScheduler
import interia_scrap
import wp_scrap
import twoja_pogoda_scrap
import interia_actual_data
import time
import sqlite3

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=2, minute=1)
def wp_pull_data():
    wp_scrap.scrap()
    print('pomyślnie zapisano wp')
    

@scheduler.scheduled_job('cron', hour=13, minute=2)
def others_pull_data():
    twoja_pogoda_scrap.scrap()
    interia_scrap.scrap()
    print('pomyślnie zapisano twoja pogoda i interia')


def download_data():
    conn = sqlite3.connect('forecast_data.db')
    c = conn.cursor()

    c.execute(
        "SELECT temperature, emoji, time, date FROM wp WHERE date = date('now') ORDER BY date ASC") 
    data_wp = c.fetchall()

    c.execute(
        "SELECT temperature, emoji, time, date FROM twoja_pogoda WHERE date = date('now') ORDER BY date ASC") 
    data_twoja_pogoda = c.fetchall()

    c.execute(
        "SELECT temperature, emoji, time, date FROM interia WHERE date = date('now') ORDER BY date ASC") 
    data_interia = c.fetchall()

    conn.close()

    return data_interia, data_wp, data_twoja_pogoda

# @scheduler.scheduled_job('cron', minute='0')
# def pull():
#     real_temp, real_emoji, hour = interia_actual_data.scrap_data()
#     data_interia, data_wp, data_twoja_pogoda = download_data()

# @scheduler.scheduled_job('cron', minute='1')
# def compare_data():
#     real_temp, real_emoji, hour = interia_actual_data.scrap_data()
#     data_interia, data_wp, data_twoja_pogoda = download_data()

#     real_int_temp = int(real_temp)
#     hour_index = hour

#     interia_temp = data_interia[hour_index][0]
#     interia_emoji = data_interia[hour_index][1]

#     wp_temp = data_wp[hour_index][0]
#     wp_emoji = data_wp[hour_index][1]

#     twoja_pogoda_temp = data_twoja_pogoda[hour_index][0]
#     twoja_pogoda_emoji = data_twoja_pogoda[hour_index][1]

#     diff_interia_temp = abs(interia_temp - real_int_temp)
#     diff_wp_temp = abs(wp_temp - real_int_temp)
#     diff_twoja_pogoda_temp = abs(twoja_pogoda_temp - real_int_temp)

#     min_diff = min(diff_interia_temp, diff_wp_temp, diff_twoja_pogoda_temp)

#     closest_sources = []
#     if diff_interia_temp == min_diff:
#         closest_sources.append("Interia")
#         closest_temperature = interia_temp
#     if diff_wp_temp == min_diff:
#         closest_sources.append("WP")
#         closest_temperature = wp_temp
#     if diff_twoja_pogoda_temp == min_diff:
#         closest_sources.append("Twoja pogoda")
#         closest_temperature = twoja_pogoda_temp

#     if len(closest_sources) == 1:
#         closest_source = closest_sources[0]
#     else:
#         closest_source = ", ".join(closest_sources[:len(closest_sources)])

#     closest_sources_emoji = []
#     closest_sources_name_emoji = []
#     if real_emoji == interia_emoji:
#         closest_sources_emoji.append(interia_emoji)
#         closest_sources_name_emoji.append('Interia')
#     if real_emoji == wp_emoji:
#         closest_sources_emoji.append(wp_emoji)
#         closest_sources_name_emoji.append('WP')
#     if real_emoji == twoja_pogoda_emoji:
#         closest_sources_emoji.append(twoja_pogoda_emoji)
#         closest_sources_name_emoji.append('Twoja pogoda')

#     if len(closest_sources_emoji) == 1 and len(closest_sources_name_emoji) == 1:
#         closest_source_emoji = closest_sources_emoji[0]
#         closest_source_name_emoji = closest_sources_name_emoji[0]
#     elif len(closest_sources_emoji) > 1 and len(closest_sources_name_emoji) > 1:
#         closest_source_emoji = ", ".join(closest_sources_emoji)
#         closest_source_name_emoji = ", ".join(closest_sources_name_emoji)
#     else:
#         closest_source_emoji = "❌"
#         closest_source_name_emoji = "❌"


#     conn = sqlite3.connect('general_scoring.db')
#     c = conn.cursor()

#     c.execute("INSERT INTO general_scoring (real_temperature, real_emoji, the_closest_temp_portal_name, the_closest_emoji_portal_name, portal_emoji, closest_temperature, min_difference) VALUES (?, ?, ?, ?, ?, ?, ?)",
#               (real_int_temp, real_emoji, closest_source, closest_source_name_emoji, closest_source_emoji, closest_temperature, min_diff))

#     conn.commit()
#     conn.close

#     scoring(closest_source, min_diff,
#             closest_source_name_emoji, closest_source_emoji)


# def scoring(closest_source: str, min_diff: int, closest_source_name_emoji: str, closest_source_emoji: str):
#     points = 0

#     conn = sqlite3.connect('general_scoring.db')
#     c = conn.cursor()
#     c.execute("SELECT wp_scoring, interia_scoring, twoja_pogoda_scoring, currently_date FROM scoring ORDER BY currently_date DESC, time DESC")
#     db_points = c.fetchone()

#     wp_scoring = db_points[0]
#     interia_scoring = db_points[1]
#     twoja_pogoda_scoring = db_points[2]

#     c.execute("SELECT the_closest_emoji_portal_name FROM general_scoring ORDER BY currently_date DESC, time DESC")
#     portal_emoji_name_tuple = c.fetchone()

#     for name in portal_emoji_name_tuple:
#         if name == 'WP':
#             wp_scoring += 25
#         elif name == 'Twoja pogoda':
#             twoja_pogoda_scoring += 25
#         elif name == 'Interia':
#             interia_scoring += 25

#     if min_diff == 0:
#         points = 10
#     elif min_diff == 1:
#         points = 8
#     elif min_diff == 2:
#         points = 6
#     elif min_diff == 3:
#         points = 4
#     elif min_diff == 4:
#         points = 2
#     elif min_diff == 5:
#         points = 1
#     elif min_diff > 5 <= 8:   
#         points = 0.5
#     else:
#         points = 0

#     sources_list = closest_source.split(', ')
#     sources_list_len = len(sources_list)

#     for i in range(sources_list_len):

#         if sources_list[i] == 'WP':
#             wp_scoring += points
#         elif sources_list[i] == 'Twoja pogoda':
#             twoja_pogoda_scoring += points
#         elif sources_list[i] == 'Interia':
#             interia_scoring += points
#         else:
#             print("No portal is accurate")

#     c.execute("INSERT INTO scoring (wp_scoring, interia_scoring, twoja_pogoda_scoring) VALUES (?, ?, ?)",
#               (wp_scoring, interia_scoring, twoja_pogoda_scoring))

#     conn.commit()
#     conn.close

scheduler.start()


try:
    while True:
        time.sleep(60)
except (KeyboardInterrupt):
    scheduler.shutdown()
    print("Scheduler shutdown successfully.")
