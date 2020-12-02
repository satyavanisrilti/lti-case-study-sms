from sqlalchemy import Column, String, Date, DateTime
from .base import Base
import bcrypt


class Auth(Base):
    __tablename__ = "auth"

    # Feilds for Auth table
    username = Column('username', String(10), primary_key=True)
    password = Column('password', String, nullable=False)
    last_login = Column('last_login', DateTime, nullable=False)

    def insert(self, session):
        """
            Insert new record to DB.
        """

        self.password = bcrypt.hashpw(self.password.encode('utf-8'),
                                      bcrypt.gensalt())

        session.add(self)

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return False

        return True

    @staticmethod
    def is_auth_successful(session, username, password):
        """
            Validates the authentication
        """
        auth_obj = session.query(Auth).get(username)

        if auth_obj is None:
            return False

        if bcrypt.checkpw(password.encode('utf-8'), auth_obj.password):
            return True
        else:
            return False
