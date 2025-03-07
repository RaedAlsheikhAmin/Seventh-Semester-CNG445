from flask import *

app = Flask(__name__)

app.secret_key = "secret"

articles = [("A1", "A1 Title", "A1 Description"), ("A2", "A2 Title", "A2 Description"), ("A3", "A3 Title", "A3 Description")]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.post("/applylogin")
def applylogin():
    #DB should be checked to make sure that we have a valid user
    session["username"] = request.form["username"]
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

@app.route("/showarticles")
def showArticles():
    if "username" in session:
        return render_template("articles.html", articles = articles)
    else:
        return redirect(url_for("index"))

@app.get("/showarticle")
def showArticle():
    if "username" in session:
        articleid = request.args.get("articleid")
        for a in articles:
            if a[0] == articleid:
                return render_template("article.html", article=a)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
