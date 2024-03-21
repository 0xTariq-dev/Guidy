#!/usr/bin/python
"""Review module"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer


class Review(BaseModel, Base):
    """Review class to store review information"""
    __tablename__ = 'reviews'
    text = Column(String(1024), nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    course_id = Column(String(60), ForeignKey('courses.id'), nullable=False)

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
