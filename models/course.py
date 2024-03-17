#!/usr/bin/python3
""" holds class Course """

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.lesson import Lesson
from models.user import User
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship

course_lessons = Table('course_lessons', Base.metadata,
                       Column('course_id', String(60),
                              ForeignKey('courses.id', onupdate='CASCADE',
                                         ondelete='CASCADE'),
                                primary_key=True),
                        Column('lesson_id', String(60),
                               ForeignKey('lessons.id', onupdate='CASCADE',
                                            ondelete='CASCADE'),
                                 primary_key=True))


class Course(BaseModel, Base):
    """Representation of Course """
    __tablename__ = 'courses'
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=False)
    lessons = relationship("Lesson",
                            secondary=course_lessons,
                            viewonly=False)
    users = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Course"""
        super().__init__(*args, **kwargs)
