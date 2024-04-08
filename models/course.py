#!/usr/bin/python3
""" holds class Course """

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.lesson import Lesson
from models.user import User
from sqlalchemy import Column, String, ForeignKey, Table, Integer
from sqlalchemy.orm import relationship


class Course(BaseModel, Base):
    """Representation of Course """
    __tablename__ = 'courses'
    title = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    length = Column(Integer, nullable=False)
    level = Column(String(60), nullable=False)
    resource_type = Column(String(60), nullable=False)
    lessons_titles = Column(String(1024), nullable=False)
    lessons = relationship("Lesson", back_populates="course", cascade="all, delete-orphan")
    reviews = relationship("Review", backref="course")
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user = relationship("User", secondary="enrollments", back_populates="courses")  # noqa

    def __init__(self, *args, **kwargs):
        """initializes Course"""
        super().__init__(*args, **kwargs)
