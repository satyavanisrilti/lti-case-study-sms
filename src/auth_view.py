from prompt_toolkit.shortcuts import input_dialog, message_dialog
from sqlalchemy.sql.functions import user
from .models.auth import Auth


def auth(session, is_admin=False):
    """
        Input: Session (SQLAlchemy), is_admin(role)
        Output: return True if auth is successcul
                else False.
    """

    # Promt user for username
    username = input_dialog(
        title='Authentication',
        text='Please type your username:').run()

    # Promt user for password
    password = input_dialog(
        title='Authentication',
        text='Please type your password:',
        password=True).run()

    try:
        # Try to fetch credentials from database
        if is_admin:
            # Defualt Username & Password
            # for Admin User Only.
            db_username = 'admin'
            db_password = '1234'
        else:
            pass
    except Exception as e:
        return False

    return (db_username == username) and (db_password == password)


def stu_auth(session, is_stu=False):
    """
        Input: Session (SQLAlchemy), is_stu(role)
        Output: return True if auth is successcul
                else False.
    """

    # Promt user for username
    username = input_dialog(
        title='Authentication',
        text='Please type your username(Roll Number):').run()

    # Promt user for password
    password = input_dialog(
        title='Authentication',
        text='Please type your password:',
        password=True).run()

    status = (Auth.is_auth_successful(session,
                                      username,
                                      password), username)
    return status
