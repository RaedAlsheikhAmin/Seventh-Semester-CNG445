import sqlite3
from sqlite3 import *

def createDB(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("CREATE TABLE user("
              "username TEXT PRIMARY KEY,"
               "password TEXT)")

    c.execute("CREATE TABLE post("
              "postid INTEGER PRIMARY KEY AUTOINCREMENT,"
              "content TEXT,"
              "username TEXT,"
              "FOREIGN KEY(username)REFERENCES user(username)")

    conn.close()

def insertRecords(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("INSERT INTO user VALUES(?, ?)", ("test1", "123"))
    c.execute("INSERT INTO user VALUES(?, ?)", ("test2", "123"))

    c.execute("INSERT INTO post(content, username) VALUES(?, ?)", ("post from test1", "test1"))
    c.execute("INSERT INTO post(content, username) VALUES(?, ?)", ("post from test2", "test2"))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    createDB("posts.db")
    insertRecords("posts.db")