from course_module import Course
from lab_course_module import LabCourse
from department_module import Department
import matplotlib.pyplot as plt


class University:

    def __init__(self, uname="?", ubranch="?"):
        self.unane = uname
        self.ubranch = ubranch
        self.departments = []

    def loadUniversity(self, file_path1, file_path2):
        departments = []
        section_flag = 0

        with open(file_path1, 'r') as dept_file:

            next(dept_file)

            for line in dept_file:
                data = line.strip().split(',')
                dcode = int(data[0].strip())
                dshortname = data[1].strip()
                dname = data[2].strip()
                department = Department(dname, dshortname, dcode)
                departments.append(department)

        with open(file_path2, 'r') as course_file:

            next(course_file)

            for line in course_file:
                data = line.strip().split(',')
                dcode = int(data[0].strip())
                ccode = data[1].strip()
                cname = data[2].strip()
                instructor = data[3].strip()
                section_num = data[4].strip()
                capacity = data[5].strip()
                registered_students = data[6].strip()

                for department in departments:
                    if dcode == department.dcode:
                        if not department.courses:
                            if section_num.startswith('L'):
                                course = LabCourse(ccode, cname)
                                course.addLabSection(section_num, capacity, registered_students, instructor)
                                department.courses.append(course)
                            else:
                                course = Course(ccode, cname)
                                course.addSection(section_num, capacity, registered_students, instructor)
                                department.courses.append(course)
                        else:
                            for course in department.courses:
                                if ccode == course.ccode:
                                    section_flag = 1
                                    course.addSection(section_num, capacity, registered_students, instructor)

                            if section_flag != 1:
                                if section_num.startswith('L'):
                                    course = LabCourse(ccode, cname)
                                    course.addLabSection(section_num, capacity, registered_students, instructor)
                                    department.courses.append(course)
                                else:
                                    course = Course(ccode, cname)
                                    course.addSection(section_num, capacity, registered_students, instructor)
                                    department.courses.append(course)
                section_flag = 0

        university = University()
        university.departments = departments

        return university

    def addDepartment(self, dname, dshortname, dcode):
        department = Department(dname, dshortname, dcode)
        self.departments.append(department)

    def printLabCourses(self):
        for department in self.departments:
            lab_courses = department.getLabCourses()

            for lab in lab_courses:
                print(lab)

    def printDepartmentSizes(self):
        sizes = []
        departments = []

        for department in self.departments:
            department_size = 0
            departments.append(department.dshortname)

            for course in department.courses:
                department_size += course.getTotalRegistered()

            sizes.append(department_size)

        if sizes:
            plt.pie(sizes, labels=departments)
            plt.title('Department Sizes')
            plt.show()
        else:
            print("No departments to display.")

    def printInstructorCourses(self):
        courses_list = []
        counter = 1

        name = input("Enter the name of the Instructor: ")

        for department in self.departments:
            for course in department.courses:
                for section_id, section_info in course.sections.items():  # Use .items() to get key-value pairs
                    if section_info["instructor_name"] == name:  # Access the instructor_name from the section_info dictionary
                        courses_list.append(course)

        if len(courses_list) > 1:
            print("Instructor {}".format(
                name) + " teaches multiple courses. Please select which course to print details for: ")
            for course in courses_list:
                print("{})".format(counter) + " " + course.cname)
                counter = counter + 1

            choice = int(input("\n\nYour choice: "))

            print(courses_list[choice - 1])
        else:
            if courses_list:
                print(courses_list[0])

        if not courses_list:
            print("The instructor was not found!!")

    def printUnpopulatedCourses(self):
        for department in self.departments:
            courses_list = department.getUnpopulatedCourses()

            print("Department Name: {}".format(department.dname))

            if not courses_list:
                print("No unpopulated courses found for the department\n")
            else:
                for course in courses_list:
                    print(course)

    def printMultiSectionCourses(self):
        for department in self.departments:
            courses_list = department.getMultisectionCourses()

            print("Department Name: {}".format(department.dname))

            if not courses_list:
                print("No multi-section courses found for the department\n")
            else:
                for course in courses_list:
                    print(course)

    def printTopCourses(self):
        for department in self.departments:
            courses_list = department.getTopCourses()

            print("Department Name: {}".format(department.dname))

            if not courses_list:
                print("No top courses found for the department\n")
            else:
                for course in courses_list:
                    print(course)


