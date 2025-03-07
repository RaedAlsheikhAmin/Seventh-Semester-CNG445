import sqlite3

def createDatabase(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = 1")

    c.execute("CREATE TABLE IF NOT EXISTS STUDENT("
              "stdID INTEGER PRIMARY KEY,"
              "stdName TEXT,"
              "major TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS COURSE("
              "courseCode TEXT PRIMARY KEY,"
              "courseNAME TEXT)")

    c.execute("CREATE TABLE IF NOT EXISTS STUDENT_COURSE("
              "stdID INTEGER,"
              "courseCode TEXT,"
              "semester INTEGER,"
              "grade TEXT,"
              "FOREIGN KEY (stdID) REFERENCES STUDENT(stdID),"
              "FOREIGN KEY (courseCode) REFERENCES COURSE(courseCode),"
              "PRIMARY KEY(stdID, courseCode, semester))")

    conn.commit()
    conn.close()

def insertRecord(dbname):
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    students = [(1, 'Olivia Ethan', 'CNG'), (2, 'William Harper', 'CNG'), (3, 'Sophia Charlatte', 'EEE')]
    c.executemany("INSERT INTO STUDENT VALUES(?, ?, ?)", students)

    courses = [('CNG140', 'C Programming'), ('CNG213', 'Data Structures'), ('CNG315', 'Algorithms')]
    c.executemany("INSERT INTO COURSE VALUES (?,?)", courses)

    student_courses = [(1, "CNG140", 20192, "AA"), (2, "CNG140", 20192, "BB"), (2, "CNG213", 20201, "CC")]
    c.executemany("INSERT INTO STUDENT_COURSE VALUES(?,?,?,?)", student_courses)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    dbname = input("Enter the name of the database: ")
    #createDatabase(dbname)
    #insertRecord(dbname)

    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    c.execute("SELECT * FROM STUDENT")
    row = c.fetchone()
    while row != None:
        print("ID: {}, Name: {}, Major: {}".format(row[0], row[1], row[2]))
        row = c.fetchone()

    #Print the names of the students who took CNG140 in 20192
    c.execute("SELECT s.stdName FROM STUDENT s, STUDENT_COURSE sc WHERE s.stdID = sc.stdID AND sc.courseCode = 'CNG140' AND sc.semester = 20192")
    rows = c.fetchall()
    for row in rows:
        print("Student Name: {}".format(row[0]))

    #Print the history of the courses for a particular student
    c.execute("SELECT s.stdName, c.courseName, sc.grade, sc.semester FROM STUDENT s, STUDENT_COURSE sc, COURSE c WHERE s.stdID = sc.stdID AND sc.courseCode = c.courseCode AND s.stdID= 2")
    rows = c.fetchall()
    for row in rows:
        print("Student Name: {}, Course Name: {}, Grade: {}, Semester: {}".format(row[0], row[1], row[2], row[3]))

    #Print the courses ordered by course name in descending order
    c.execute("SELECT * FROM COURSE ORDER BY courseName DESC")
    row = c.fetchone()
    while row != None:
        print("Code: {}, Name: {}".format(row[0], row[1]))
        row = c.fetchone()

    #Print the number of students for each major
    c.execute("SELECT major, COUNT(*) FROM STUDENT GROUP BY major")
    rows = c.fetchall()
    for row in rows:
        print("Major: {}, Number of students: {}".format(row[0], row[1]))

    #Print the number of students for each major with more than 1 student
    c.execute("SELECT major, COUNT(*) FROM STUDENT GROUP BY major HAVING COUNT(*) > 1")
    rows = c.fetchall()
    for row in rows:
        print("Major: {}, Number of students: {}".format(row[0], row[1]))

    keyword = input("Enter a keyword to search: ")
    c.execute("SELECT * FROM STUDENT WHERE stdName LIKE '%{}%'".format(keyword))
    rows = c.fetchall()
    for row in rows:
        print("ID: {}, Name: {}, Major: {}".format(row[0], row[1], row[2]))


    #Update the name of student "William" to "Will.
    c.execute("UPDATE STUDENT SET stdName = 'Will' WHERE stdID = ?", (2,))
    conn.commit()

    c.execute("SELECT * FROM STUDENT")
    row = c.fetchone()
    while row != None:
        print("ID: {}, Name: {}, Major: {}".format(row[0], row[1], row[2]))
        row = c.fetchone()

    conn.close()