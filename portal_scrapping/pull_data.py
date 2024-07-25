from apscheduler.schedulers.background import BackgroundScheduler
import interia_scrap, wp_scrap, twoja_pogoda_scrap, interia_actual_data
import time

scheduler = BackgroundScheduler()

@scheduler.scheduled_job('cron', hour=2, minute=1)
def wp_pull_data():
    wp_scrap.scrap()

@scheduler.scheduled_job('cron', hour=13, minute=1)
def others_pull_data():
    twoja_pogoda_scrap.scrap()
    interia_scrap.scrap()

@scheduler.scheduled_job('interval', minutes=30)
def actual_data():
    temp, emoji = interia_actual_data.scrap_data()
    print(temp, emoji)

    

scheduler.start()

try:
    while True:
        time.sleep(1)  
except (KeyboardInterrupt):
    scheduler.shutdown()
    print("Scheduler shut down successfully.")