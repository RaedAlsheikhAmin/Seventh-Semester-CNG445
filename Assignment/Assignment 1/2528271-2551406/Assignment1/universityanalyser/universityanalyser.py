from Course import Course
from University import University
import sys

def printMenu():
    print("\nWelcome to University Analyzer")
    print("1. Print all lab courses")
    print("2. Print department sizes")
    print("3. Print instructor courses")
    print("4. Print unpopulated courses")
    print("5. Print multi-section courses")
    print("6. Print top courses")
    print("0. Exit")

if __name__ == '__main__':

    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 3:
        print("please use  python universityanalyser.py departments.txt courses.txt in the terminal to take the Arguments")
        sys.exit(1)

    # Get file names from command-line arguments
    departments_file = sys.argv[1]
    courses_file = sys.argv[2]

    # Create a University instance
    university = University("METU","NCC")

    # loading data into the university object
    try:
        university.LoadUniversityData(departments_file, courses_file)
        print("Data loaded successfully.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

    # main loop to handle menu selection
    while True:
        printMenu()
        choice = input("Enter your choice: ")

        if choice == "1":
            print("\nLab Courses:")
            university.PrintLabCourses()

        elif choice == "2":
            print("\nDepartment Sizes:")
            university.PrintDepartmentSizes()

        elif choice == "3":
            instructor_name = input("Enter the instructor's name: ")
            university.PrintInstructorCourses(instructor_name)

        elif choice == "4":
            print("\nUnpopulated Courses:")
            university.PrintUnpopulatedCourses()

        elif choice == "5":
            print("\nMulti-section Courses:")
            university.PrintMultisectionCourses()

        elif choice == "6":
            print("\nTop Courses:")
            university.PrintTopCourses()

        elif choice == "0":
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")





