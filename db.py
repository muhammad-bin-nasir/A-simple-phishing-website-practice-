import sqlite3

conn = sqlite3.connect('phish_sim.db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM credentials')
rows = cursor.fetchall()

for row in rows:
    print(row)

conn.close()
