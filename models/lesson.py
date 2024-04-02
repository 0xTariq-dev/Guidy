#!/usr/bin/python
"""Lesson module"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship


class Lesson(BaseModel, Base):
    """Lesson class to store lesson information"""
    __tablename__ = 'lessons'
    title = Column(String(128), nullable=False)
    description = Column(String(4096), nullable=False)
    course_id = Column(String(60), ForeignKey('courses.id'), nullable=False)
    course = relationship("Course", back_populates="lessons")
    resources = relationship("Resource", back_populates="lesson")

    def __init__(self, *args, **kwargs):
        """initializes Lesson"""
        super().__init__(*args, **kwargs)
