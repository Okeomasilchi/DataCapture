#!/usr/bin/python3
""" holds class SurveyCategory"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class SurveyCategory(BaseModel, Base):
    __tablename__ = 'surveycategory'

    SurveyCategoryID = Column(String(60), primary_key=True)
    SurveyID = Column(String(60), ForeignKey('surveys.SurveyID'))
    category_id = Column(String(60), ForeignKey('customcategory.CategoryID'))
    survey = relationship('Survey')
    category = relationship('CustomCategory')


    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
