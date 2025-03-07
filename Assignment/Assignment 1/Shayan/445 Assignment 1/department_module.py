from course_module import Course
from lab_course_module import LabCourse


class Department:

    def __init__(self, dname="?", dshortname="?", dcode=0):
        self.dname = dname
        self.dshortname = dshortname
        self.dcode = dcode
        self.courses = []

    def addCourse(self, ccode, cname, ctype):
        if ctype == "Normal":
            course = Course(ccode, cname)
            self.courses.append(course)
        elif ctype == "Lab":
            lab_course = LabCourse(ccode, cname)
            self.courses.append(lab_course)

    def getLabCourses(self):
        lab_courses = []

        for item in self.courses:
            if isinstance(item, LabCourse):
                lab_courses.append(item)

        return lab_courses

    def getTotalLabCapacity(self):
        lab_courses = self.getLabCourses()
        total_capacity = 0

        for item in lab_courses:
            total_capacity += item.getLabCapacity()

        return total_capacity

    def getUnpopulatedCourses(self):
        unpopulated_courses = []

        for item in self.courses:
            registered_students = item.getTotalRegistered()

            if registered_students < 5:
                unpopulated_courses.append(item)

        return unpopulated_courses

    def getMultisectionCourses(self):
        multisection_courses = []

        for item in self.courses:
            if isinstance(item, LabCourse):
                if item.getNumSections() > 1 or item.getNumLabSection() > 1:
                    multisection_courses.append(item)
            elif isinstance(item, Course):
                if item.getNumSections() > 1:
                    multisection_courses.append(item)

        return multisection_courses

    def getTopCourses(self):
        top_courses = []
        max_val = 0

        for item in self.courses:
            num_students = item.getTotalRegistered()

            if num_students > max_val:
                max_val = num_students
                top_courses = [item]
            elif num_students == max_val:
                top_courses.append(item)

        return top_courses


