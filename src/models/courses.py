from sqlalchemy import Column, String, Date, DateTime, Integer
from .base import Base


class Course(Base):
    __tablename__ = "courses"

    # Feilds for Courses Table
    course_id = Column('course_id', String(10), primary_key=True)
    name = Column('name', String(64), nullable=False)
    duration_in_hours = Column('duration_in_hours', Integer, nullable=False)
    fee = Column('fee', Integer, nullable=False)
    date_of_creation = Column('date_of_creation', DateTime, nullable=False)

    def __repr__(self) -> str:
        return "| {:<28} | {:<28} | {:<18} | {:<18} | {:<28} |".format(
                     self.course_id, self.name,
                     self.duration_in_hours, 
                     self.fee, 
                     self.date_of_creation.strftime("%b-%d-%Y %H:%M:%S"))

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
    def view_courses(session):
        """
            Input: Session
            Output: Query Result
        """

        result = session.query(Course).all()

        return result

    @staticmethod
    def print_header():
        """
            Prints the header of the courses table
        """
        header = \
         "| {:<28} | {:<28} | {:<18} | {:<18} | {:<28} |".format("COURSE_ID",
                                                                 "NAME",
                                                                 "DURATION (Hrs)",
                                                                 "FEE (INR)",
                                                                 "REGISTRATION_DATE")
        print(header, "\n", "_"*(len(header)), "\n")
