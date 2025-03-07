import sqlite3
def insertsampledata(dbname):
    conn=sqlite3.connect(dbname)
    c=conn.cursor()

    c.execute("""INSERT INTO User (username, password, f_name, email, isAdmin)
                VALUES 
                ('admin', 'Admin1234', 'Admin User', 'admin@game.metu.edu.tr', 1),
                ('user1', 'User12345', 'Regular User', 'user1@example.com', 0),
                ('user2', 'User23456', 'Another User', 'user2@example.com', 0);""")

    c.execute("""INSERT INTO Genre (name)
                    VALUES 
                ('Action'),
                ('Adventure'),
                ('Role-Playing'),
                ('Simulation'),
                ('Strategy');"""
                                        )

    c.execute("""INSERT INTO Game (title, price, description, isFullrelease, username)
                    VALUES 
                    ('Epic Adventure', 19.99, 'A thrilling adventure game.', 1, 'user1'),
                    ('Strategy Master', 29.99, 'A challenging strategy game.', 1, 'user2'),
                    ('Fantasy RPG', 24.99, 'An immersive role-playing game.', 0, 'user1');""")

    c.execute("""INSERT INTO Game_Genres (gameID, genreID)
                VALUES 
                (1, 2), -- Epic Adventure -> Adventure
                (2, 5), -- Strategy Master -> Strategy
                (3, 3); -- Fantasy RPG -> Role-Playing""")
    conn.commit()





if __name__ == '__main__':
    insertsampledata(dbname="GameWebsite.db")