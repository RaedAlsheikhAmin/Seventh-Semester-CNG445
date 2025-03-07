from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.get("/gethint")
def gethint():
    names = ["Anna", "Brittany", "Cinderella", "Diana", "Eva", "Fiona",
             "Gunda", "Hege", "Inga", "Johanna", "Kitty", "Linda", "Nina",
             "Ophelia", "Petunia", "Amanda", "Raquel", "Cindy", "Doris",
             "Eve", "Evita", "Sunniva", "Tove", "Unni", "Violet", "Liza",
             "Elizabeth", "Ellen", "Wenche", "Vicky"]

    suggestions = []
    keyword = request.args.get("q", None)
    if keyword != None:
        for name in names:
            if keyword.lower() == name[0:len(keyword)].lower():
                suggestions.append(name)

    return ", ".join(suggestions)

if __name__ == "__main__":
    app.run()