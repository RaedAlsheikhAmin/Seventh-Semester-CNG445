import re
from Department import Department
from Course import Course, LabCourse
import matplotlib.pyplot as plt

class University:
    __slots__=["uname","ubranch","departments"]
    def __init__(self, name, branch):#Initialize a University object with a university name and branch.

        self.uname = name
        self.ubranch = branch
        self.departments = []

    def AddDepartment(self, dcode, dshortname, dname):#Add a department to the university by creating a Department object.

        department = Department(dcode, dshortname, dname)
        self.departments.append(department)

    def LoadUniversityData(self, departments_file, courses_file):#Load department and course data from files to populate university structure.
        """
    This code starts by loading department data from a file,
    skipping the header and reading each line to create and add Department objects to the university.
    Then, it processes the course data from another file,
    also skipping the header and checking each line for formatting issues or incorrect data types.
    If a line is valid, it finds the matching department based on dcode. If the department exists,
    it checks if the course section is a lab or a regular section.
    Lab sections are added to existing LabCourse objects or new ones are created if needed.
    Regular sections are similarly handled for Course objects. If a department isn't found for a course,
    it logs a message saying the department doesn't exist.
        """
        with open(departments_file, 'r') as df:
            next(df)  # Skip header line because we don't need it
            for line in df:
                dcode, dshortname, dname = line.strip().split(',')
                self.AddDepartment(int(dcode), dshortname, dname)

        # Load courses and add them to the appropriate departments
        with open(courses_file, 'r') as cf:
            next(cf)  # Skip header line
            for line in cf:
                parts = line.strip().split(',')
                if len(parts) != 7:
                    print(f"Skipping invalid line: {line}")
                    continue  # Skip lines that don't have the correct number of fields

                dcode, course_code, course_name, instructor, section, capacity, registered = parts
                try:
                    dcode = int(dcode)
                    capacity = int(capacity)
                    registered = int(registered)
                except ValueError:
                    print(f"Skipping line with invalid data types: {line}")
                    continue  # Skip lines with incorrect data types

                # checking the format of the course
                course_code = course_code.strip()
                if not re.match(r"^[A-Z]{3,4}\s?\d{3,4}$", course_code):
                    print(f"Skipping invalid course code format: {course_code}")
                    continue

                # Find department by department code
                department = next((dept for dept in self.departments if dept.dcode == dcode), None)

                if department:
                    if "Lab" in section or section.startswith("Lab"):
                        # Add lab section to an existing LabCourse or create a new one
                        lab_course = next(
                            (c for c in department.courses if isinstance(c, LabCourse) and c.ccode == course_code),
                            None)
                        if not lab_course:
                            department.addCourse(course_code, course_name, True)
                            lab_course = department.courses[-1]  # Get the newly added LabCourse
                        lab_course.AddLabSection(section, capacity, registered, instructor)
                    else:
                        # Add regular section to an existing Course or create a new one
                        course = next(
                            (c for c in department.courses if isinstance(c, Course) and c.ccode == course_code),
                            None)
                        if not course:
                            department.addCourse(course_code, course_name, False)
                            course = department.courses[-1]  # Get the newly added Course
                        course.addSection(section, capacity, registered, instructor)
                else:
                    print("Department doesn't exist in the file")

    def PrintLabCourses(self):#Print all lab courses across the university, showing department and course details.
        for department in self.departments:
            lab_courses = department.GetLabCourses()
            if lab_courses:
                print(f"Department: {department.dname} ({department.dshortname})")
                print(f"Total Lab Capacity: {department.GetTotalLabCapacity()}")
                for lab_course in lab_courses:
                    print(lab_course)
                print("-" * 50)

    def PrintDepartmentSizes(self):#Display a pie chart of the department sizes based on the total number of registered students.
        department_names = [dept.dshortname for dept in self.departments]
        sizes = []
        for dept in self.departments:
            total_registered = 0
            for course in dept.courses:
                if isinstance(course, Course):
                    total_registered += course.GetTotalCapacity()
            sizes.append(total_registered)
        plt.pie(sizes, labels=department_names)
        plt.title('Department Sizes')
        plt.show()

    def PrintInstructorCourses(self, instructor_name):#Print the details of courses taught by a specified instructor.
        found_courses = []
        for department in self.departments:
            for course in department.courses:
                for section, details in course.sections.items():
                    if details[0] == instructor_name:
                        found_courses.append((course, section, details))

        if not found_courses:
            print(f"No courses found for instructor: {instructor_name}")
            return

        print(f"Courses taught by {instructor_name}:")
        for idx, (course, section, details) in enumerate(found_courses, start=1):
            print(f"{idx}. {course.ccode} - {course.cname} (Section {section})")

        choice = int(input(f"Enter the course number to view details (1-{len(found_courses)}): ")) - 1
        selected_course, section, details = found_courses[choice]
        print(selected_course)

    def PrintUnpopulatedCourses(self):#printing the details of the courses with less than 5 registered students
        for department in self.departments:
            unpopulated_courses = department.GetUnpopulatedCourses()
            if unpopulated_courses:
                print(f"Department: {department.dname} ({department.dshortname}) - Unpopulated Courses:")
                for course in unpopulated_courses:
                    print(course)
                print("-" * 50)
            else:
                print(f"Department: {department.dname} ({department.dshortname}) has no unpopulated courses.")

    def PrintMultisectionCourses(self):#Print details of courses with more than one section or lab section in each department.

        for department in self.departments:
            multisection_courses = department.GetMultisectionCourses()
            if multisection_courses:
                print(f"Department: {department.dname} ({department.dshortname}) - Multi-section Courses:")
                for course in multisection_courses:
                    print(course)
                print("-" * 50)
            else:
                print(f"Department: {department.dname} ({department.dshortname}) has no multi-section courses.")

    def PrintTopCourses(self):#Print the courses with the highest number of registered students in each department. (still not working perfectly check it before submitting)

        for department in self.departments:
            top_courses = department.GetTopCourses()
            print(f"Department: {department.dname} ({department.dshortname}) - Top Course(s):")
            for course in top_courses:
                print(course)
            print("-" * 50)

    def __str__(self):

        dept_info = "\n".join(str(dept) for dept in self.departments)
        return f"University Name: {self.uname}\nBranch: {self.ubranch}\nDepartments:\n{dept_info}"
