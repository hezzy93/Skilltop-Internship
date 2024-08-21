#!/usr/bin/python3
""" holds class User """

import jwt
import datetime
import os
from dotenv import load_dotenv

from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import bcrypt
import models
from models.base_model import BaseModel, Base

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

class User(BaseModel, Base):
    """Representation of a user
    
    User_role:
        0(Employee), 1(Super Admin), 2(Admin),
        3(Manager), 4(Sales Employee), 5(Finance)
    Active:
        0(deactivate) 1(Active)
    Deleted:
        0(false) 1(true)
    """
    __tablename__ = 'users'

    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_role = Column(Integer, default=0, nullable=False)
    active = Column(Integer, default=1, nullable=False)
    deleted = Column(Integer, default=0, nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets attributes with special handling for password and email"""
        if name == "password":
            value = bcrypt.hashpw(value.lower().encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # Convert password to lowercase
        if name == "email":
            value = value.lower()  # Convert email to lowercase
        super().__setattr__(name, value)

    # JWT Authentication

    def generate_auth_token(self, expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60):
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in),
            'iat': datetime.datetime.utcnow(),
            'sub': self.email
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


    @staticmethod
    def verify_auth_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return None  # valid token, but expired
        except jwt.InvalidTokenError:
            return None  # invalid token
