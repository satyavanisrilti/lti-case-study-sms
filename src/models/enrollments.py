from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .base import Base
from datetime import datetime
from .courses import Course
from .students import Student


class Enrollment(Base):
    __tablename__ = "enrollments"

    # Feilds for Enrollment Table
    course_id = Column('course_id', String(10),
                       ForeignKey(Course.course_id),
                       primary_key=True)

    roll_number = Column('roll_number', String(10),
                         ForeignKey(Student.roll_number),
                         primary_key=True)

    date_of_enrollment = Column('date_of_enrollment',
                                DateTime,
                                nullable=False)

    def __repr__(self) -> str:
        return "|{:<21} |{:<21} |{:<21} |".format(self.course_id,
                                                  self.roll_number,
             self.date_of_enrollment.strftime("%b-%d-%Y %H:%M:%S"))

    def insert(self, session):
        """
            Input: Session
            Output: Status of transaction.
        """

        session.add(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return False

        return True

    @staticmethod
    def view_all_enrollments(session):
        """
            Input: Session
            Output: Query Result
        """

        result = session.query(Enrollment).all()

        return result

    @staticmethod
    def view_student_enrollments(session):
        """
            Querys the enrollments with given roll number.
        """
        roll_number = session.student_username
        result = session.query(Enrollment).filter_by(roll_number=roll_number).all()

        return result

    @staticmethod
    def print_header():
        """
            Prints the header of Enrollments table
        """
        header = "|{:<21} |{:<21} |{:<21} |".format("COUSER_ID",
                                                    "ROLL_NUMBER",
                                                    "REGISTRATION_DATE")
        print(header, '\n', "_"*(len(header)), "\n")
