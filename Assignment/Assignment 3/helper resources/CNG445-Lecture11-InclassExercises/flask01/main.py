from flask import *
from markupsafe import *

app = Flask(__name__)

@app.route("/")
def index_page():
    return render_template("index.html")

@app.route("/helloworld")
def hello_world():
    #Return the string to be displayed on a web browser
    return "<p>Hello World</>"

@app.route("/welcome/<username>")
def welcome_username(username):
    return f"<p>Welcome {escape(username)} </p>"

@app.route("/getname", methods = ["GET", "POST"])
def get_name():
    if request.method == "POST":
        fullname = request.form["fullname"]
        #KeyError will be raised
    elif request.method == "GET":
        fullname = request.args.get("fullname", "")
    return render_template("welcome.html", fullname = fullname)

"""
@app.post("/getname")
def get_name_post():
    fullname = request.form["fullname"]
    return render_template("welcome.html", fullname=fullname)

@app.get("/getname")
def get_name_get():
    fullname = request.args.get("fullname", "")
    return render_template("welcome.html", fullname=fullname)
"""

@app.route("/getlang")
def print_languages():
    langlist = ["C", "C++", "Java", "Python"]
    return render_template("languages.html", langlist = langlist)

if __name__ == "__main__":
    app.run()