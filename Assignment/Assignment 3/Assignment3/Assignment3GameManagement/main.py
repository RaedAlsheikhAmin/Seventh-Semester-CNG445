
from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key = '123'

#this function will take the username using GET method in Ajax and it will check if the username exists in the database or not in real-time
@app.route("/check_username", methods=["GET"]) #using AJAX for real time updates
def check_username():
    username = request.args.get("q", "")  # Get 'q' parameter from the request
    print(username)
    if username=="":
        return "Username is required."
    try:
        # Connect to the database
        conn = sqlite3.connect("GameWebsite.db")
        cursor = conn.cursor()

        # Checking if the username exists
        cursor.execute("SELECT username FROM User WHERE username = ?", (username,))
        result = cursor.fetchone()
    finally:
        conn.close()

    if result:
        return "Username is already taken."
    else:
        return "Username is available."


#this function will take the email using GET method in AJAX and it will check if it exists in the databse or not in realtime

@app.route("/check_email", methods=["GET"])#using AJAX for real time updates
def check_email():
    email = request.args.get("q", "").strip()# for removing whitespaces
    if not email:
        return "Email is required."

    try:
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()
        c.execute("SELECT email FROM User WHERE email = ?", (email,))
        if c.fetchone():
            return "Email is already registered."
        return "Email is available."
    finally:
        conn.close()



@app.route("/")
@app.route("/index")
def index():
    try:
        # Fetch all published games that all the users can see it
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()
        #to have the genres combo box
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()
        c.execute("""
            SELECT G.title, G.description, G.price, GROUP_CONCAT(Gr.name) AS genres
            FROM Game G
            LEFT JOIN Game_Genres GG ON G.gameID = GG.gameID
            LEFT JOIN Genre Gr ON GG.genreID = Gr.genreID
            GROUP BY G.gameID
        """)
        games = c.fetchall()
    finally:
        conn.close()

    return render_template("index.html", games=games, genres=genres)


@app.route("/Register", methods=["GET", "POST"])
def Register():
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")
        full_name = request.form.get("fullName", "")
        email = request.form.get("email", "")

        #just to debug some issues
        print(f"Received: username={username}, password={password}, full_name={full_name}, email={email}")

        # Validate inputs
        if not username or not password or not full_name or not email:
            return render_template("Register.html")

        # Check for existing username
        try:
            conn = sqlite3.connect("GameWebsite.db")
            c = conn.cursor()
            c.execute("SELECT username FROM User WHERE username = ?", (username,))
            if c.fetchone():
                return render_template("Register.html")

            # Insert new user into the database
            is_admin = 1 if email.endswith("@game.metu.edu.tr") else 0
            c.execute("""
                INSERT INTO User (username, password, f_name, email, isAdmin)
                VALUES (?, ?, ?, ?, ?)
            """, (username, password, full_name, email, is_admin))
            conn.commit()
            #this functionality was done in the graduation project, that is why i am using it here
        except sqlite3.Error:
            return render_template("Register.html")
        finally:
            conn.close()

        return redirect(url_for("registration_confirmation"))
    return render_template("Register.html")

@app.route("/registration_confirmation")
def registration_confirmation():
    return render_template("confirmation.html")

@app.route("/login", methods=["POST"])
def login():
    #To get the values using post method
    username = request.form["username"]
    password = request.form["password"]

    # Connect to the database
    conn = sqlite3.connect("GameWebsite.db")
    c = conn.cursor()

    # Verify user credentials
    c.execute("SELECT username, isAdmin FROM User WHERE username = ? AND password = ?", (username, password))
    row = c.fetchone()
    conn.close()


    if row: #that means the user if found in the query
        session["username"] = row[0]
        session["isAdmin"] = row[1] == 1
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("index",msg="check your user name and password again")) #this will be appended to the url

@app.route("/logout")
def logout():
    session.pop("username","")#to make sure the session is cleared.
    return redirect(url_for("index"))

@app.route("/dashboard")
def dashboard():
    # to Ensure the user is logged in before continuing to the dashboard
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]
    is_admin = session["isAdmin"]

    conn = sqlite3.connect("GameWebsite.db")
    c = conn.cursor()

    if is_admin:
        # Admin dashboard: fetch genres
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()
        conn.close()
        return render_template("admin_dashboard.html", username=username, genres=genres)
    else:
        # User dashboard: fetch user's games
        c.execute("SELECT gameID, title, price FROM Game WHERE username = ?", (username,))
        games = c.fetchall()
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()  # Fetch genres for game creation
        conn.close()
        return render_template("user_dashboard.html", username=username, games=games, genres=genres)




@app.route("/delete-game/<int:game_id>", methods=["GET"])
def delete_game(game_id):
    # Ensure the user is logged in
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    try:
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()

        # Ensure the game belongs to the logged-in user
        c.execute("DELETE FROM Game WHERE gameID = ? AND username = ?", (game_id, username))
        c.execute("DELETE FROM Game_Genres WHERE gameID = ?", (game_id,))
        conn.commit()
    finally:
        conn.close()

    return redirect(url_for("manage_games"))


@app.route("/manage_games", methods=["GET", "POST"])
def manage_games():
    # Ensure the user is logged in
    if "username" not in session  or  session.get("isAdmin"): #to make sure the admin can not change anything for the user
        return redirect(url_for("index"))

    username = session["username"]

    try:
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()

        # Fetch all genres for the form
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()

        # If form is submitted, handle game creation
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            price = request.form.get("price", "").strip()
            description = request.form.get("description", "").strip()
            is_fullrelease = request.form.get("isFullrelease", "0") == "1"
            selected_genres = request.form.getlist("genres")  # List of genre IDs

            # Validate required fields
            if not title or not price or not selected_genres:
                return render_template("manage_games.html", genres=genres, error="Title, price, and at least one genre are required.")

            try:
                # Insert the game into the Game table
                c.execute("""
                    INSERT INTO Game (title, price, description, isFullrelease, username)
                    VALUES (?, ?, ?, ?, ?)
                """, (title, float(price), description, is_fullrelease, username))
                game_id = c.lastrowid  # Get the new game's ID

                # Insert game-genre relationships
                for genre_id in selected_genres:
                    c.execute("INSERT INTO Game_Genres (gameID, genreID) VALUES (?, ?)", (game_id, int(genre_id)))

                conn.commit()
            except sqlite3.Error as e:
                conn.rollback()
                return render_template("manage_games.html", genres=genres, error=f"Database error: {e}")

        # Fetch all games published by the user
        c.execute("""
            SELECT G.gameID, G.title, G.price, G.description, G.isFullrelease, GROUP_CONCAT(Gr.name) AS genres
            FROM Game G
            LEFT JOIN Game_Genres GG ON G.gameID = GG.gameID
            LEFT JOIN Genre Gr ON GG.genreID = Gr.genreID
            WHERE G.username = ?
            GROUP BY G.gameID
        """, (username,))
        games = c.fetchall()

    finally:
        conn.close()

    return render_template("manage_games.html", genres=genres, games=games)


#try to use ajax here for later on.
@app.route("/search", methods=["GET"])
def search_games():
    keywords = request.args.get("keywords", "").strip()
    genre_id = request.args.get("genre", "all")

    try:
        conn = sqlite3.connect("GameWebsite.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Fetch all genres
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()

        # Prepare query to fetch games
        query = """
            SELECT G.gameID, G.title, G.description, G.price, Gr.name AS genre_name
            FROM Game G
            LEFT JOIN Game_Genres GG ON G.gameID = GG.gameID
            LEFT JOIN Genre Gr ON GG.genreID = Gr.genreID
        """
        conditions = []
        params = []

        if keywords:
            conditions.append("G.title LIKE ?")
            params.append(f"%{keywords}%")

        if genre_id != "all":
            conditions.append("Gr.genreID = ?")
            params.append(genre_id)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " ORDER BY Gr.name, G.title"

        c.execute(query, params)
        games = c.fetchall()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        genres = []
        games = []
    finally:
        conn.close()

    # Group games by genre (only include genres with matching games)
    grouped_games = {}
    for game in games:
        genre_name = game["genre_name"]
        if genre_name not in grouped_games:
            grouped_games[genre_name] = []
        grouped_games[genre_name].append(game)

    return render_template(
        "search_results.html",
        grouped_games=grouped_games,
        keywords=keywords,
        genres=genres,
    )


@app.route("/profile", methods=["GET", "POST"])
def profile():
    # Ensure the user is logged in
    if "username" not in session:
        return redirect(url_for("index"))

    username = session["username"]

    try:
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()

        # Fetch user details for the profile form
        c.execute("SELECT username, f_name, email, password FROM User WHERE username = ?", (username,))
        user = c.fetchone()

        if not user:
            return redirect(url_for("index"))  # If user not found, redirect to home page

        if request.method == "POST":
            # Update profile details
            full_name = request.form.get("full_name", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "").strip()

            if not full_name or not email or not password:
                return render_template("profile.html", error="All fields are required.", user=user)

            try:
                c.execute("""
                    UPDATE User
                    SET f_name = ?, email = ?, password = ?
                    WHERE username = ?
                """, (full_name, email, password, username))
                conn.commit()
                success = "Profile updated successfully."
            except sqlite3.Error as e:
                return render_template("profile.html", error=f"Database error: {e}", user=user)

    finally:
        conn.close()

    return render_template("profile.html", user=user, success=locals().get("success"))

@app.route("/manage_genres", methods=["GET", "POST"])
def manage_genres():
    # Ensure the user is logged in and is an admin
    if "username" not in session or not session.get("isAdmin"):
        return redirect(url_for("index"))

    try:
        conn = sqlite3.connect("GameWebsite.db")
        c = conn.cursor()

        # Handle genre creation
        if request.method == "POST":
            genre_name = request.form.get("genre_name", "").strip()

            if not genre_name:
                # Reload the page with an error message
                c.execute("SELECT genreID, name FROM Genre")
                genres = c.fetchall()
                return render_template("manage_genres.html", genres=genres, error="Genre name cannot be empty.")

            try:
                # Check if the genre already exists
                c.execute("SELECT genreID FROM Genre WHERE name = ?", (genre_name,))
                if c.fetchone():
                    c.execute("SELECT genreID, name FROM Genre")
                    genres = c.fetchall()
                    return render_template("manage_genres.html", genres=genres, error="Genre already exists.")

                # Insert new genre into the database
                c.execute("INSERT INTO Genre (name) VALUES (?)", (genre_name,))
                conn.commit()
            except sqlite3.Error as e:
                c.execute("SELECT genreID, name FROM Genre")
                genres = c.fetchall()
                return render_template("manage_genres.html", genres=genres, error=f"Database error: {e}")

        # Fetch all genres for the list
        c.execute("SELECT genreID, name FROM Genre")
        genres = c.fetchall()

    finally:
        conn.close()

    return render_template("manage_genres.html", genres=genres)


@app.route("/game/<int:game_id>", methods=["GET"])
def game_details(game_id):
    try:
        conn = sqlite3.connect("GameWebsite.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        # Fetch game details
        c.execute("""
            SELECT G.gameID, G.title, G.description, G.price, G.isFullrelease, GROUP_CONCAT(Gr.name, ', ') AS genres
            FROM Game G
            LEFT JOIN Game_Genres GG ON G.gameID = GG.gameID
            LEFT JOIN Genre Gr ON GG.genreID = Gr.genreID
            WHERE G.gameID = ?
            GROUP BY G.gameID
        """, (game_id,))
        game = c.fetchone()

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        game = None
    finally:
        conn.close()

    # Check if game exists
    if not game:
        pass
    # Render game details page
    return render_template("game_details.html", game=game)



if __name__=='__main__':
    app.run()