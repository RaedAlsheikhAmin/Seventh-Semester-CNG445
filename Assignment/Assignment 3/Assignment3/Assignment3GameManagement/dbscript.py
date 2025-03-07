#this file will be responsible for creating the database.
import sqlite3

def createDB(dbname):
    conn = sqlite3.connect(dbname) #connection to the database
    c = conn.cursor() #for starting executing

    #if Not exists command to make sure i will not face errors if I run this file multiple times
    #Not null to make sure all the values are included
    c.execute(" CREATE TABLE IF NOT EXISTS User ("
               " username TEXT Primary KEY NOT NULL," 
               " password TEXT NOT NULL," 
               " f_name TEXT NOT NULL," 
               " email TEXT NOT NULL," 
               " isAdmin BOOLEAN NOT NULL DEFAULT 0 )") #By default, will be assigned to 0 => not admin

    # GameTable creation
    c.execute(" CREATE TABLE IF NOT EXISTS Game ("
              "  gameID INTEGER PRIMARY KEY AUTOINCREMENT,"
              "  title TEXT NOT NULL,"
              "  price REAL NOT NULL," 
              "  description TEXT,"
              "  isFullrelease BOOLEAN NOT NULL DEFAULT 0," 
              " username TEXT NOT NULL," 
              " FOREIGN KEY (username) REFERENCES User (username))" )

    # Creating Genres table
    c.execute(" CREATE TABLE IF NOT EXISTS Genre ("
              " genreID INTEGER PRIMARY KEY AUTOINCREMENT," 
              " name TEXT  NOT NULL )" )

    # Creating Game-Genres table for many-to-many relationship
    c.execute("  CREATE TABLE IF NOT EXISTS Game_Genres ("
              "  gameID INTEGER NOT NULL," 
              "  genreID INTEGER NOT NULL,"
              "  PRIMARY KEY (gameID, genreID),"
              "  FOREIGN KEY (gameID) REFERENCES Game (gameID),"
              "  FOREIGN KEY (genreID) REFERENCES Genre (genreID))" )

    conn.close()
if __name__ == "__main__":
    createDB("GameWebsite.db")