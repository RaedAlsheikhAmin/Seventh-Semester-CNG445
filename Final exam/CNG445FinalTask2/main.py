from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    conn = sqlite3.connect("department.db")
    cursor = conn.cursor()
    cursor.execute("SELECT academicsemester FROM courselecturer group by academicsemester")
    result= cursor.fetchall()
    availableemester= result
    availableemester.sort()
    conn.close()
    return render_template("index.html",semesters=availableemester)


@app.route("/semesterdetails/<int:academicsemester>",methods=["GET"])
def semesterdetails(academicsemester):
    conn = sqlite3.connect("department.db")
    cursor = conn.cursor()
    cursor.execute("SELECT coursecode,count(section) FROM courselecturer where academicsemester=? group by coursecode", (academicsemester,))
    result= cursor.fetchall()
    print(result)
    return render_template("semesterdetails.html",Courses=result)

@app.route("/Course/<coursecode>",methods=["GET"])
def coursedetails(coursecode):
    conn = sqlite3.connect("department.db")
    cursor = conn.cursor()
    cursor.execute("SELECT section, lecturername FROM courselecturer, lecturer where coursecode=? ", (coursecode,))
    result= cursor.fetchall()
    print(result)
    return render_template("coursedetails.html",Sections=result)



if __name__=='__main__':
    app.run()