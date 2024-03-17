#!/usr/bin/env python
"""This is the user module."""

import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import bcrypt


class User(BaseModel, Base):
    """User class to interact with the API."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    review = relationship("Review", backref="user")
    courses = relationship("Course",
                           secondary="enrollments",
                           back_populates="users")
    
    def __init__(self, *args, **kwargs):
        """User class constructor"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, k, v):
        """Hash the password before setting it."""
        v = bcrypt.hashpw(
            v.encode(), bcrypt.gensalt()
            ) if k == 'password' else super().__setattr__(k, v)
