#!./venv/bin/python3

from __future__ import unicode_literals
import os
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import button_dialog
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.models import auth, base, students, courses
from src import admin_view, student_view


# Clear Screen
name = os.name
if name == 'nt':
    os.system("cls")
else:
    os.system("clear")

# Database Configuration
engine = create_engine("sqlite:///smsapp.db")
base.Base.metadata.create_all(engine, checkfirst=True)
Session = sessionmaker(bind=engine)
session = Session()

# Choose the role
is_admin_role = button_dialog(
    title='Welcome to Student Management System',
    text='Please choose your role. Continue as?',
    buttons=[
        ('Admin', True),
        ('Student', False),
    ],
).run()

# Display Co-responding view of the role
if is_admin_role:
    admin_view.main(session)
else:
    student_view.main(session)
