import sqlite3

# Get input file path from user
file = input("Enter the path to the input file: ")
termin = []
description = []

# Process the text file and extract terms and descriptions
def text_processing(file=file):

    c = 0

    f = open(file, "r", encoding="utf-8")
    lines = f.readlines()

    for line in lines:
        l = 0
        for term in line.split(" - "):
            if c % 2 == 0: 
                termin.append(term.strip())
            else:
                description.append(term.strip())
            c += 1; 

    f.close()

# Create database and table 
def create_database():
    conn = sqlite3.connect("kmb_bot.db")

    cursor = conn.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS bedingungen (id INTEGER PRIMARY KEY AUTOINCREMENT, term TEXT, description TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, username TEXT, first_name TEXT, last_name TEXT)")

    for i in range(len(termin)):
        cursor.execute("INSERT INTO bedingungen (term, description) VALUES (?, ?)", (termin[i], description[i]))

    conn.commit()
    conn.close()
    print("Database and table created, data inserted successfully.")


def get_random_term():
    '''
    Return a random term and its description and ID from the database 
    as a list of tuples [(id, term, description)]

    Get values by index:
        record = get_random_term()
        print(record[0][0]) # ID
        print(record[0][1]) # Term
        print(record[0][2]) # Description
    
    '''

    conn = sqlite3.connect('kmb_bot.db')
    cursor = conn.cursor()

    query = "SELECT * FROM bedingungen ORDER BY RANDOM() LIMIT 1"

    cursor.execute(query)
    record = cursor.fetchall()

    conn.close()
    return record


record = get_random_term()
print(record)

