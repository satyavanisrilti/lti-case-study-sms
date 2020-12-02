from os import stat
from sqlalchemy import Column, String, Date, DateTime
from .base import Base
from datetime import datetime


class Student(Base):
    __tablename__ = "students"

    # Feilds for Students Table
    roll_number = Column('roll_number', String(10), primary_key=True)
    name = Column('name', String(32), nullable=False)
    dob = Column('dob', Date, nullable=False)
    registration_date = Column('registration_date', DateTime, nullable=False)

    def __repr__(self) -> str:
        return "|{:<18} |{:<18} |{:<21} |{:<21} |".format(
                self.roll_number,
                self.name,
                self.dob.strftime("%d-%b-%Y"),
                self.registration_date.strftime("%b-%d-%Y %H:%M:%S"))

    def insert(self, session):
        """
            Input: Session
            Output: Status of transaction.
        """

        self.dob = datetime.strptime(self.dob, "%d-%M-%Y")

        session.add(self)
        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return False

        return True

    @staticmethod
    def view_students(session):
        """
            Input: Session
            Output: Query Result
        """

        result = session.query(Student).all()

        return result

    @staticmethod
    def print_header():
        """
            Prints the header of the students table
        """
        header = "| {:<18} | {:<18} | {:<21} | {:<21} |".format("ROLL_NUMBER",
                                                                "NAME",
                                                                "DATE-OF-BIRTH",
                                                                "REGISTRATION_DATE")
        print(header, '\n', "_"*(len(header)), "\n")
