#!/usr/bin/env python
"""This is the user module."""

import sqlalchemy
import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

enrollments = Table('enrollments', Base.metadata,
    Column('user_id', String(60), ForeignKey('users.id')),
    Column('course_id', String(60), ForeignKey('courses.id'))
)


class User(BaseModel, Base):
    """User class to interact with the API."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    resource_type = Column(String(60), nullable=False)
    review = relationship("Review", backref="user")
    courses = relationship("Course",
                           secondary="enrollments",
                           back_populates="user")

    def __init__(self, *args, **kwargs):
        """User class constructor"""
        super().__init__(*args, **kwargs)

    def __setattr__(self, k, v):
        """Hash the password before setting it."""
        if k == 'password':
            v = bcrypt.hashpw(
                v.encode(), bcrypt.gensalt()
                )
        super().__setattr__(k, v)
