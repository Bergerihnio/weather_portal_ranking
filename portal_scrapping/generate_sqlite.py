import sqlite3

conn = sqlite3.connect('interia.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS interia
        (temperature INTEGER,
        time TEXT DATETIME,
        emoji TEXT,
        date TEXT DEFAULT (date('now', '+2 days')),
        currently_date TEXT DEFAULT (date('now')))''')

conn.commit()
conn.close()

###################################

conn = sqlite3.connect('twoja_pogoda.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS twoja_pogoda
        (temperature INTEGER,
        time TEXT DATETIME,
        emoji TEXT,
        date TEXT DEFAULT (date('now', '+2 days')),
        currently_date TEXT DEFAULT (date('now')))''')

conn.commit()
conn.close()


