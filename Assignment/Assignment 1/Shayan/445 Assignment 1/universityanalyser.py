import sys
from university_module import University


def main():
    if len(sys.argv) != 3:
        print("Usage: python your_script.py <departments_file> <courses_file>")
        sys.exit(1)

    # Get the filenames from command-line arguments
    departments_file = sys.argv[1]
    courses_file = sys.argv[2]

    # Instantiate the university
    university = University("METU", "NCC")

    # Load university data from the files
    university = university.loadUniversity(departments_file, courses_file)

    # Menu loop
    while True:
        print("\nMenu:")
        print("1. Print All Lab Courses")
        print("2. Print Department Sizes")
        print("3. Print Instructor Courses")
        print("4. Print Unpopulated Courses")
        print("5. Print Multi-Section Courses")
        print("6. Print Top Courses")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            university.printLabCourses()
        elif choice == '2':
            university.printDepartmentSizes()
        elif choice == '3':
            university.printInstructorCourses()
        elif choice == '4':
            university.printUnpopulatedCourses()
        elif choice == '5':
            university.printMultiSectionCourses()
        elif choice == '6':
            university.printTopCourses()
        elif choice == '7':
            print("\nExiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
