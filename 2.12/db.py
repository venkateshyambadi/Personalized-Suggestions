import sqlite3

conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        mail TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        medication TEXT NOT NULL,
        days INTEGER NOT NULL                
    )
""")

conn.commit()
conn.close()

def add_user_data(mail,date, time, medication, days):
    # Ensure 'time' is converted to a string
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()    
    # Example SQL query
    time = time.strftime("%H:%M:%S")
    date = date.strftime("%Y-%m-%d")

    c.execute("""
        INSERT INTO user_data (mail, date, time, medication, days)
        VALUES (?, ?, ?, ?,?)
    """, (mail,date,time, medication, days))
    conn.commit()


def fetch_user_data(mail):
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    c.execute("SELECT * FROM user_data WHERE mail = ?", (mail,))
    user_data = c.fetchall()
    conn.close()
    return user_data

def delete_medication(mail, medication):
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    c.execute("DELETE FROM user_data WHERE mail = ? AND medication = ?", (mail, medication))
    conn.commit()
    conn.close()

def update_medication(mail, medication, days):
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    c.execute("UPDATE user_data SET days = ? WHERE mail = ? AND medication = ?", (days, mail, medication))
    conn.commit()
    conn.close()

# delete all data if the date is less than today
def all_data():
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    c.execute("DELETE FROM user_data WHERE date < date('now')")
    conn.commit()
    conn.close()