#!/usr/bin/python3
""" holds class Login """

import bcrypt

class Login:
    def __init__(self, email, hashed_password):
        self.__email = email.lower()  # Store email as lowercase
        self.__password = hashed_password  # Store hashed password

    @property
    def email(self):
        return self.__email

# verify user
    def verify_user(self, input_email, input_password):
        """Verify user inputs against the stored email and password."""
        email_match = self.__email == input_email.lower()  # Convert input email to lowercase
        password_match = bcrypt.checkpw(input_password.encode('utf-8'), self.__password.encode('utf-8'))
        return email_match and password_match

    def __repr__(self):
        """Return a string representation of the Login object."""
        return f"<Login(email={self.__email}, password={'*' * 60})>"
