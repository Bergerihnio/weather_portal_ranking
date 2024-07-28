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


conn = sqlite3.connect('wp.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS wp
        (temperature INTEGER,
        time TEXT DATETIME,
        emoji TEXT,
        date TEXT DEFAULT (date('now', '+2 days')),
        currently_date TEXT DEFAULT (date('now')))''')

conn.commit()
conn.close()

conn = sqlite3.connect('general_scoring.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS general_scoring 
        (real_temperature INTEGER,
        real_emoji TEXT,
        the_closest_temp_portal_name TEXT,
        closest_temperature INTEGER,
        the_closest_emoji_portal_name TEXT,  
        portal_emoji TEXT,
        time TEXT DEFAULT (time('now', 'localtime')),
        currently_date TEXT DEFAULT (date('now')))''')

c.execute('''CREATE TABLE IF NOT EXISTS general_scoring 
        (real_temperature INTEGER,
        real_emoji TEXT,
        the_closest_temp_portal_name TEXT,
        closest_temperature INTEGER,
        the_closest_emoji_portal_name TEXT,  
        portal_emoji TEXT,
        time TEXT DEFAULT (time('now', 'localtime')),
        currently_date TEXT DEFAULT (date('now')))''')

conn.commit()
conn.close()

