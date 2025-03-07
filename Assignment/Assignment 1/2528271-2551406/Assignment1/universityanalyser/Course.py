class Course:
    __slots__=["ccode","cname","sections"] #to make sure that the object will not have other than these attributes
    def __init__(self,ccode,cname):
        self.ccode=ccode
        self.cname=cname
        self.sections={}

    def addSection(self,SectionNo,Capacity,NumOfStudents,InstructorName): #it will add the section to the dictionary of sections
        self.sections[SectionNo] = (InstructorName, Capacity, NumOfStudents)

    def GetTotalCapacity(self):# It will go through the values of the dictionary of sections and return the index 1 which will be the capacity, which will be accumulated to collect the whole capacity for all the course.
        total_capacity = 0
        for single_capacity in self.sections.values():
            total_capacity += single_capacity[1]  # Add the capacity from each section
        return total_capacity

    def GetTotalRegistered(self):# it will return the second index of each section, which will be the students registered
        return sum(TotalRegistered[2] for section,TotalRegistered in self.sections.items() if "Lab" not in section )

    def __str__(self):
        sections_info = "\n".join(
            f"  Section {sectionNO}: Instructor: {item[0]}, Capacity: {item[1]}, Registered: {item[2]}"
            for sectionNO, item in self.sections.items()
        )
        return f"Course Code: {self.ccode}\nCourse Name: {self.cname}\nSections:\n{sections_info}"


class LabCourse(Course):
    def __init__(self, ccode, cname):
        super().__init__(ccode, cname)
        self.labSections = {} # it will be for the lab sections for each course

    def AddLabSection(self, labSectionNo, capacity, numOfStudents, instructorName):

        self.labSections[labSectionNo] = (instructorName, capacity, numOfStudents)

    def GetLabCapacity(self):#Calculate the total capacity across all lab sections of the course.

        total_capacity = 0
        for section in self.labSections.values():
            total_capacity += section[1]  # Accumulate the capacity for each lab section
        return total_capacity

    def __str__(self):#Return a string representation of the lab course, showing course code, course name,and lab section details.

        labs_info = "\n".join(
            f"  {section_no}: Instructor: {item[0]}, Capacity: {item[1]}, Registered: {item[2]}"
            for section_no, item in self.labSections.items()
        )
        return f"Course Code: {self.ccode}\nCourse Name: {self.cname}\nLab Sections:\n{labs_info}"
