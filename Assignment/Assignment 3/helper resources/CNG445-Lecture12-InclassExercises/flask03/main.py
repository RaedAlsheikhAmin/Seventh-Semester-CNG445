from flask import *
import sqlite3

app = Flask(__name__)
app.secret_key="123"

@app.route("/register")
def showRegistration():
    return render_template("registration.html")

@app.post("/applyregistration")
def applyregistration():
    try:
        agreement = request.form["agreement"]
        username = request.form["username"]
        password = request.form["pwd"]
        fullname = request.form["fullname"]
        gender = request.form["gender"]
        conn = sqlite3.connect("posts.db")
        c = conn.cursor()
        c.execute("INSERT INTO user VALUES(?,?,?,?)", (username, password, fullname, gender))
        conn.commit()
        conn.close()
        return render_template("registration.html", msg="Registration is successful! Click <a href='/index'>here</a> to login")
        #Hint: Check |safe for the template to be able to consider HTML tags
    except:
        return render_template("registration.html", msg="You need to select checkbox")

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