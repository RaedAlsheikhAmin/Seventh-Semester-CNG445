from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/getxml")
def getxml():
    xmlDoc = open("data/bookstore.xml").read()
    return Response(xmlDoc, mimetype="text/xml")

if __name__ == "__main__":
    app.run()