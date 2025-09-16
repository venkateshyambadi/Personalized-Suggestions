import sqlite3

conn = sqlite3.connect("users.db")
c = conn.cursor()
c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        password TEXT NOT NULL
        
    )
"""),
c.execute("""
    CREATE TABLE IF NOT EXISTS user_data (
        id INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        medication_name TEXT NOT NULL,
        number_of_days INTEGER NOT NULL,
        FOREIGN KEY (id) REFERENCES users (id),
        PRIMARY KEY (id)
                
    )
""")

conn.commit()
conn.close()

def add_user(name,email,age,gender,password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("INSERT INTO users (name,email,age,gender,password) VALUES (?, ?, ?,?,?)", (name,email,age,gender,password))
    conn.commit()
    conn.close()

def authenticate_user(email, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ? AND password = ?", (email, password))
    user = c.fetchone()
    conn.close()
    return user
def fetch_user(email):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = c.fetchone()
    conn.close()
    return user

def add_user_data(id, start_date, time, medication, days):
    # Ensure 'time' is converted to a string
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    time_str = time.strftime("%H:%M:%S")  # Convert to 'HH:MM:SS' format
    start_date_str = start_date.strftime("%Y-%m-%d")  # Convert date to 'YYYY-MM-DD'
    
    # Example SQL query
    c.execute("""
        INSERT INTO user_data (id, start_date, time, medication, days)
        VALUES (?, ?, ?, ?, ?)
    """, (id, start_date_str, time_str, medication, days))
    conn.commit()


def fetch_user_data(id):
    conn = sqlite3.connect("user_data.db")  # Ensure this references the correct DB
    c = conn.cursor()
    c.execute("SELECT * FROM user_data WHERE id = ?", (id,))
    user_data = c.fetchall()
    conn.close()
    return user_data
