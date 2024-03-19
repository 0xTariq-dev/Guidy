#!/usr/bin/python
"""Resource module"""

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Resource(BaseModel, Base):
    """Resource class to store resource information"""
    __tablename__ = 'resources'
    title = Column(String(128), nullable=False)
    type = Column(String(128), nullable=True)
    link = Column(String(128), nullable=False)
    lesson_id = Column(String(60), ForeignKey('lessons.id'), nullable=False)
    lesson = relationship("Lesson", back_populates="resources")

    def __init__(self, *args, **kwargs):
        """initializes Resource"""
        super().__init__(*args, **kwargs)