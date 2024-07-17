#!/usr/bin/python3
""" holds class User"""

from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
import bcrypt
import models
from models.base_model import BaseModel, Base


class User(BaseModel, Base):
    """Representation of a user """
    __tablename__ = 'users'

    name = Column(String(150), nullable=False)
    email = Column(String(200), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    user_role = Column(Integer, default=0, nullable=False, comment="0(Employee), 1(Super Admin), 2(Admin), 3(Manager), 4(Sales Employee), 5(Finance)")
    active = Column(Integer, default=1, nullable=False, comment="0(deactivate) 1(Active)")
    deleted = Column(Integer, default=0, nullable=False, comment="0(false) 1(true)")
    
    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """sets a password with bcrypt encryption"""
        if name == "password":
            value = bcrypt.hashpw(value.encode('utf-8'), bcrypt.gensalt())
        super().__setattr__(name, value)
