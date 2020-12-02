import os
import random
from datetime import datetime
from src.models.enrollments import Enrollment
from src.models.courses import Course
from src.models.students import Student
from .auth_view import auth
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit import prompt


# ----- #
# Start Helper Functions
# ----- #

def center_text(text):
    """
        Calculates center based on text length
    """
    total_terminal_columns = os.get_terminal_size().columns
    text_length = len(text)
    space_on_one_side = (total_terminal_columns - text_length)//2
    space = " " * space_on_one_side

    return space + text + space


def get_random_string(length):
    letters = "0123456789"
    result_str = ''.join(random.choice(letters) for i in range(length))
    result_str = "CR-" + result_str
    return result_str


# ----- #
# Start Validators
# ----- #

# Validates Add new Course Data
def validate_new_course(name, duration, fee):
    """
        Input: Course feilds
        Output: Tuple(Status, Message)
    """

    message = ""

    # Course Name validation
    if not (len(name) >= 3):
        message = "Course name must contain atleast 3 Characters."
        return False, message

    # Course Duration Validation
    if not(duration.isnumeric()):
        message = "Duration field has to be integer."
        return False, message

    # Course Fee Validation
    if not(fee.isnumeric()):
        message = "Fee feild has to be integer."
        return False, message

    return True, message


# ----- #
# Start Admin Prompt Functionalities
# ----- #

# Admin Prompt actions functionality
def prompt_add_new_course(session):
    """
        Allow admin to add new courses to db.
    """
    course_name = prompt(" Name of the Course?: ",
               bottom_toolbar="\n"+ center_text(
                   "Student Management System (Logged In as @Administrator)") + "\n")
    
    course_duration = prompt(" Duration of the Course? (In Hours): ", 
               bottom_toolbar="\n"+ center_text(
                   "Student Management System (Logged In as @Administrator)") + "\n")

    course_fee = prompt(" Fee for the Course? (INR): ",
               bottom_toolbar="\n"+ center_text(
                   "Student Management System (Logged In as @Administrator)") + "\n")

    # Validates input
    status, message = validate_new_course(course_name, course_duration, course_fee)
    if status:
        Course(course_id=get_random_string(10),
               name=course_name,
               duration_in_hours=course_duration,
               fee=course_fee,
               date_of_creation=datetime.now()).insert(session)
        print("\nAdd Course Successful!")
        admin_prompt(session)
    else:
        print("\n ", message, " Please try again!")
        prompt_add_new_course(session)


def prompt_view_courses(session):
    """
        Shows the available courses in db.
    """
    result = Course.view_courses(session)
    Course.print_header()

    for i in result:
        print(i)

    admin_prompt(session)


def prompt_view_student(session):
    """
        View the details of all students
    """
    result = Student.view_students(session)
    Student.print_header()

    for i in result:
        print(i)

    admin_prompt(session)


def prompt_view_enrollments(session):
    """
        Displays the course enrollments data
    """
    data = Enrollment.view_all_enrollments(session)

    if len(data) < 1:
        print("\nNo enrollments were found!")
        admin_prompt(session)
    else:
        Enrollment.print_header()
        for i in data:
            print(i)
        admin_prompt(session)


def admin_prompt(session):
    """
        Starts Receving input from user.
    """
    while True:
        print("\nWelcome Admin.")
        print("\n Choose one option to continue.")
        print("""
            1. Add a new Course
            2. View Student
            3. View Courses
            4. View Enrollments
            5. Exit
        """)
        text = prompt("user@admin> ",
               bottom_toolbar="\n" + center_text(
                   "Student Management System (Logged In as @Administrator)") + "\n")

        if text == "1":
            prompt_add_new_course(session)
        elif text == "2":
            prompt_view_student(session)
        elif text == "3":
            prompt_view_courses(session)
        elif text == "4":
            prompt_view_enrollments(session)
        elif text == "5":
            exit()
        else:
            print("\nInvalid Option! Please try again.")


def main(session):
    """
        Entry Point for admin view.
    """

    # Authenticate admin user
    while True:
        if auth(session, is_admin=True):
            break
        else:
            message_dialog(
                title='Authentication Failed',
                text='Invalid Username/Password. Press ENTER to try again.').run()

    # Start Admin Prompt
    admin_prompt(session)
