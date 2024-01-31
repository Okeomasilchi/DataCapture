#!/usr/bin/python3
""" holds class SurveyCategory"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import relationship


class SurveyCategory(BaseModel, Base):
    """
    Represents a mapping between a survey and a custom category.
    """

    __tablename__ = 'surveycategory'

    survey_id = Column(String(60), ForeignKey('surveys.id'), nullable=False)
    category_id = Column(String(60), ForeignKey('customcategory.id'),
                         nullable=False
                         )

    survey = relationship('Survey', cascade="all, delete")
    category = relationship('CustomCategory', cascade="all, delete")

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)