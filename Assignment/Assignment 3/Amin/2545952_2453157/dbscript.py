import sqlite3

conn = sqlite3.connect("database.db")

c = conn.cursor()

c.execute("""CREATE TABLE User (
    username TEXT PRIMARY KEY NOT NULL,
    password TEXT NOT NULL,
    fullname TEXT NOT NULL,
    email TEXT NOT NULL,
    telno TEXT NOT NULL
)""")

c.execute(""" CREATE TABLE Category (
    cid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    cname TEXT NOT NULL
)""")

c.execute(""" CREATE TABLE Advertisement (
    aid INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    is_active INTEGER NOT NULL,
    username TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (username) REFERENCES User(username),
    FOREIGN KEY (category_id) REFERENCES Category(cid)
)""")
categories = [('Clothes',), ('Technology',), ('Cars',), ('Food',), ('Drink',)]

c.executemany('INSERT INTO Category(cname) VALUES (?)',categories)


conn.commit()
conn.close()
