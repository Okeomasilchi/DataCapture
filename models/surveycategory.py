#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class SurveyCategory(BaseModel, Base):
    __tablename__ = 'SurveyCategory'
    SurveyCategoryID = Column(String(60), primary_key=True)
    SurveyID = Column(String(60), ForeignKey('Survey.SurveyID'))
    CategoryID = Column(String(60), ForeignKey('CustomCategory.CategoryID'))
    survey = relationship('Survey')
    category = relationship('CustomCategory')

    def __init__(self, *args, **kwargs):
        """initializes state"""
        super().__init__(*args, **kwargs)
