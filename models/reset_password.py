#!/usr/bin/python3
""" holds class ResetPassword """

import bcrypt
from itsdangerous import URLSafeTimedSerializer
from os import getenv
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv('SECRET_KEY')
SECURITY_PASSWORD_SALT = getenv('SECURITY_PASSWORD_SALT')

class ResetPassword:
    @staticmethod
    def generate_reset_token(email):
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        return serializer.dumps(email, salt=SECURITY_PASSWORD_SALT)

    @staticmethod
    def verify_reset_token(token, expiration=3600):
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        try:
            email = serializer.loads(
                token,
                salt=SECURITY_PASSWORD_SALT,
                max_age=expiration
            )
        except Exception:
            return None
        return email

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
