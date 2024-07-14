import sqlite3

conn = sqlite3.connect('interia_temperatures.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS interia_temperatures
        (temperature INTEGER,
        time TEXT DATETIME,
        emoji TEXT,
        date TEXT DEFAULT (date('now', '+2 days')),
        currently_date TEXT DEFAULT (date('now')))''')

conn.commit()
conn.close()


