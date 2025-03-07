class Course:

    def __init__(self, ccode=0, cname="?"):
        self.ccode = ccode
        self.cname = cname
        self.sections = {}

    def __str__(self):
        course_name = "Course Name: {}\n".format(self.cname)
        course_code = "Course Code: {}\n".format(self.ccode)

        all_sections_info = ""

        for section in self.sections:
            section_info = (
                "Section No: {}\n"
                "  Capacity: {}\n"
                "  Registered Students: {}\n"
                "  Instructor Name: {}\n\n"
            ).format(section, self.sections[section]["capacity"], self.sections[section]["registered_students"],
                     self.sections[section]["instructor_name"])
            all_sections_info += section_info

        return course_name + course_code + all_sections_info

    def addSection(self, sectionNo, capacity, registeredStudents, instructor):
        section_info = {
            "capacity": capacity,
            "registered_students": registeredStudents,
            "instructor_name": instructor
        }

        self.sections[sectionNo] = section_info

    def getTotalCapacity(self):
        total_capacity = 0

        for section in self.sections:
            total_capacity += self.sections[section]["capacity"]

        return total_capacity

    def getTotalRegistered(self):
        total_registered = 0

        for section in self.sections:
            total_registered += int(self.sections[section]["registered_students"])

        return total_registered

    def getNumSections(self):
        number = 0

        for section in self.sections:
            number += 1

        return number
