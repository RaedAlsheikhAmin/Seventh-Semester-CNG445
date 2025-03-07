from course_module import Course


class LabCourse(Course):

    def __init__(self, ccode="0", cname="?"):
        Course.__init__(self, ccode, cname)
        self.labsections = {}

    def __str__(self):
        course_name = "Course Name: {}\n".format(self.cname)
        course_code = "Course Code: {}\n".format(self.ccode)

        all_sections_info = ""

        # Print details of normal sections
        for section in self.sections:
            section_info = (
                "Section No: {}\n"
                "  Capacity: {}\n"
                "  Registered Students: {}\n"
                "  Instructor Name: {}\n\n"
            ).format(section, self.sections[section]["capacity"], self.sections[section]["registered_students"],
                     self.sections[section]["instructor_name"])
            all_sections_info += section_info

        # Print details of lab sections
        for section in self.labsections:
            section_info = (
                "Lab Section No: {}\n"
                "  Capacity: {}\n"
                "  Registered Students: {}\n"
                "  Instructor Name: {}\n\n"
            ).format(section, self.labsections[section]["capacity"], self.labsections[section]["registered_students"],
                     self.labsections[section]["instructor_name"])
            all_sections_info += section_info

        return course_name + course_code + all_sections_info

    def addLabSection(self, sectionNo, capacity, registeredStudents, instructor):
        lab_section_info = {
            "capacity": capacity,
            "registered_students": registeredStudents,
            "instructor_name": instructor
        }

        self.labsections[sectionNo] = lab_section_info

    def getLabCapacity(self):
        total_capacity = 0

        for section in self.labsections:
            total_capacity += self.labsections[section]["capacity"]

        return total_capacity

    def getNumSections(self):
        number = 0

        for section in self.sections:
            number += 1

        return number

    def getNumLabSection(self):
        number = 0

        for section in self.labsections:
            number += 1

        return number
