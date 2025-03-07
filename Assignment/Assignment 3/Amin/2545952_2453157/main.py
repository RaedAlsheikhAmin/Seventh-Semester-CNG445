from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3

app = Flask(__name__)
app.secret_key = "the_secret_key"


@app.route("/", methods=["GET", "POST"])
def home_page():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT username,password FROM User WHERE username=? AND password=?", (username, password))
        row = c.fetchone()
        conn.close()
        if row != None:
            session["user"] = username
            return redirect(url_for('home_page'))  # if user exists
        else:
            return redirect(url_for("home_page", msg="Wrong username or password"))  # if user doesn't exist




    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT cid,cname FROM Category")  # for the combobox
    category_names = c.fetchall()
    c.execute(
        "SELECT Advertisement.title, Advertisement.description, Category.cname, Advertisement.is_active, Advertisement.aid , User.fullname, Category.cid "
        "FROM Advertisement "
        "INNER JOIN Category ON Advertisement.category_id = Category.cid "
        "INNER JOIN User ON Advertisement.username=User.username"
    )
    advertisements = c.fetchall()
    conn.close()

    if 'user' not in session:
        msg = request.args.get("msg", "")
        return render_template("index.html",
                               logged_in=0, msg=msg, categories=category_names, advertisements=advertisements)
    else:
        print(session['user'])
        return render_template("index.html",
                               logged_in=1, categories=category_names, advertisements=advertisements)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    if request.method == "POST":
        try:
            c.execute("INSERT INTO User (username, password, fullname, email, telno) VALUES (?, ?, ?, ?, ?)",
                      (request.form['username'], request.form['password'], request.form['full_name'],
                       request.form['email'], request.form['phone_number']))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.rollback()  # otherwise database is locked
            return render_template("register.html", msg="This username is already in use!")
        return render_template("info.html",
                               message="Success")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")


@app.route("/advertisement", methods=["GET", "POST"])
def advertisement():
    if request.method == "POST":
        title=request.form["title"]
        description=request.form["description"]
        category_id=request.form["category"]
        username=session["user"]
        conn=sqlite3.connect('database.db')
        c=conn.cursor()
        c.execute("INSERT INTO Advertisement (title,description,is_active,username,category_id) VALUES (?,?,?,?,?)",(title,description,1,username,category_id))
        conn.commit()
        conn.close()
        return redirect(url_for('advertisement'))



    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT cid,cname FROM Category") # for the combobox
    category_names = c.fetchall()
    username=session['user']
    c.execute(
        "SELECT Advertisement.title, Advertisement.description, Category.cname, Advertisement.is_active, Advertisement.aid "
        "FROM Advertisement "
        "INNER JOIN Category ON Advertisement.category_id = Category.cid "
        "WHERE Advertisement.username = ?",
        (username,)
    )
    advertisements=c.fetchall()
    conn.close()
    return render_template("advertisement.html",categories=category_names,advertisements=advertisements)

@app.route("/active_deactive")
def active_deactive():
    aid = request.args.get('aid')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT is_active FROM Advertisement WHERE aid=?", (aid,))
    state=c.fetchone()
    if(state[0]==0):
        new_state=1
    else:
        new_state=0

    c.execute("UPDATE Advertisement SET is_active=? WHERE aid=?", (new_state, aid))
    conn.commit()
    conn.close()
    return redirect(url_for('advertisement'))


@app.route("/profile", methods=["GET", "POST"])
def profile():
    if request.method=="POST":
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute("UPDATE User SET username=?, password=?, fullname=?, email=?, telno=? WHERE username=?",
                      (request.form['username'], request.form['password'], request.form['full_name'],
                       request.form['email'], request.form['phone_number'], session['user']))
            c.execute("UPDATE Advertisement SET username=? WHERE username=?", (request.form['username'], session['user']))
            session['user'] = request.form['username']
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.rollback()  # otherwise database is locked
            conn.close()
            return redirect(url_for('profile',msg="Username has already taken!"))
        return redirect(url_for('profile', msg="Successfully updated your profile!"))

    msg = request.args.get("msg", "")
    username=session['user']
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT username,password,fullname,email,telno " 
              "FROM User WHERE username=?",(username,))
    user_details=c.fetchone()
    conn.close()
    default_data = {
        'username': user_details[0],
        'password': user_details[1],
        'fullname': user_details[2],
        'email': user_details[3],
        'telno': user_details[4],
    }
    return render_template('profile.html', default_data=default_data,msg=msg)

@app.route("/details")
def details():
    aid = request.args.get('aid')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(
        "SELECT Advertisement.title, Advertisement.description, Category.cname, User.fullname , User.email, User.telno  "
        "FROM Advertisement "
        "INNER JOIN Category ON Advertisement.category_id = Category.cid "
        "INNER JOIN User ON Advertisement.username=User.username "
        "WHERE Advertisement.aid = ?",
        (aid,)
    )
    advertisement_details=c.fetchone()
    conn.close()
    return render_template('details.html',details=advertisement_details)



if __name__ == "__main__":
    app.run(debug=True)
