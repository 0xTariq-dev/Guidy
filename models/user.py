#!/usr/bin/env python
"""This is the user module."""

import sqlalchemy
import bcrypt
from flask_login import UserMixin
from sqlalchemy import Column, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

enrollments = Table('enrollments', Base.metadata,
                    Column('user_id', String(60), ForeignKey('users.id')),
                    Column('course_id', String(60), ForeignKey('courses.id'))
                    )


class User(BaseModel, Base, UserMixin):
    """User class to interact with the API."""
    __tablename__ = 'users'
    email = Column(String(128), nullable=False, unique=True)
    username = Column(String(20), nullable=False, unique=True)
    _password = Column('password', String(128), nullable=False)
    first_name = Column(String(60), nullable=False)
    last_name = Column(String(60), nullable=False)
    active = Column(Boolean, default=True)
    authenticated = Column(Boolean, default=False)
    review = relationship("Review", backref="user")
    courses = relationship("Course",
                           secondary="enrollments",
                           back_populates="users")

    def __init__(self, *args, **kwargs):
        """User class constructor"""
        super().__init__(*args, **kwargs)

    @property
    def password(self):
        """Password getter method."""
        return self._password

    @password.setter
    def password(self, value):
        """Password setter method."""
        value = value.encode() if isinstance(value, str) else value
        self._password = bcrypt.hashpw(value, bcrypt.gensalt())

    def check_password(self, password):
        """Password validation method."""
        return bcrypt.checkpw(password.encode(), self._password.encode())

    @property
    def is_authenticated(self):
        """User authentication method."""
        return self.authenticated

    @property
    def is_active(self):
        """User active method."""
        return self.active

