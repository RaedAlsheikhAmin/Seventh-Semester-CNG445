from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key="123"

@app.route("/")
@app.route("/index")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"])
    else:
        return render_template("index.html")

@app.post("/login")
def login():
    username = request.form["username"]
    pwd = request.form["pwd"]
    conn = sqlite3.connect("posts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM user WHERE username=? AND password=?", (username, pwd))
    row = c.fetchone()
    if row != None:
        session["username"] = username
    conn.close()
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username","")
    return redirect(url_for("index"))

@app.route("/posts")
def seeposts():
    if "username" in session:
        conn = sqlite3.connect("posts.db")
        c = conn.cursor()
        c.execute("SELECT * FROM post WHERE username=?", (session["username"],))
        records = c.fetchall()
        conn.close()
        return render_template("posts.html", records = records)
    else:
        return redirect(url_for("index"))
if __name__ == "__main__":
    app.run()