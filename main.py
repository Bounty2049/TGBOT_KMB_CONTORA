import sqlite3


f = open("Bedingungen.txt", "r", encoding="utf-8")

lines = f.readlines()

termin = []
description = []
c = 0

for line in lines:
    for term in line.split(" - "):
        if c % 2 == 0: 
            termin.append(term.strip())
        else:
            description.append(term.strip())
        c += 1; 


# Create database and table 
conn = sqlite3.connect("terms.db")

cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS bedingungen (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT, description TEXT)")

for i in range(len(termin)):
    cursor.execute("INSERT INTO bedingungen (term, description) VALUES (?, ?)", (termin[i], description[i]))

cursor.execute("SELECT * FROM bedingungen")
tables = cursor.fetchall()
for table in tables:
    print(f"ID: {table[0]}, Term: {table[1]}, Description: {table[2]}")
    print()

conn.close()
print("Database and table created, data inserted successfully.")