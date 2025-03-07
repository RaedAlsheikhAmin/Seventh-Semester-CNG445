from Course import Course, LabCourse

class Department:
    __slots__=["dcode","dshortname","dname","courses"]
    def __init__(self, dcode="o", dshortname="?", dname="?"):#Initialize a Department object with a department code, short name, and full name.

        self.dcode = dcode
        self.dshortname = dshortname
        self.dname = dname
        self.courses = []  # List to store Course and LabCourse objects

    def addCourse(self, ccode, cname, isLabCourse):#Create and add a Course or LabCourse to the department.

        course = LabCourse(ccode, cname) if isLabCourse else Course(ccode, cname)
        self.courses.append(course)

    def GetLabCourses(self):#Retrieve all courses in the department that have lab sections, it will loop through the courses objects and filter the courses that belong to lab class

        return [course for course in self.courses if isinstance(course, LabCourse)]

    def GetTotalLabCapacity(self):#Calculate the total capacity of all lab sections in the department.

        total_lab_capacity = sum(course.GetLabCapacity() for course in self.GetLabCourses())
        return total_lab_capacity

    def GetUnpopulatedCourses(self):#Retrieve a list of courses with fewer than `threshold` registered students.

        threshold=5
        unpopulated_courses = []
        for course in self.courses:
            if course.GetTotalRegistered() < threshold:
                unpopulated_courses.append(course)
        return unpopulated_courses

    def GetMultisectionCourses(self):# Retrieve a list of courses with more than one lecture or lab section.

        multisection_courses = []
        for course in self.courses:
            if len(course.sections) > 1 or (isinstance(course, LabCourse) and len(course.labSections) > 1):
                multisection_courses.append(course)
        return multisection_courses

    def GetTopCourses(self):

        """
            Retrieve and print the courses with the highest number of registered students,
            excluding the number of registered students in lab sections.
            """
        if not self.courses:
            return []  # Return an empty list if there are no courses

        # Step 1: Find the maximum number of registered students in any non-lab course
        max_registered = 0
        for course in self.courses:
            if isinstance(course, Course) and not isinstance(course, LabCourse):
                total_registered = course.GetTotalRegistered()
                if total_registered > max_registered:
                    max_registered = total_registered

        # Step 2: Collect all courses that have the highest registered student count
        top_courses = []
        for course in self.courses:
            if isinstance(course, Course) and not isinstance(course, LabCourse):
                if course.GetTotalRegistered() == max_registered:
                    top_courses.append(course)

        return top_courses

    def __str__(self):# Return a string representation of the department, including department code, name, and a list of courses.

        courses_info = "\n".join(str(course) for course in self.courses)
        return f"Department Code: {self.dcode}\nDepartment Name: {self.dname} ({self.dshortname})\nCourses:\n{courses_info}"
