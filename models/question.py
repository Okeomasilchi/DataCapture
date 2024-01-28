#!/usr/bin/python
""" holds class City"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    __tablename__ = 'Question'
    QuestionID = Column(String(60), primary_key=True)
    QuestionText = Column(Text)
    Options = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('Survey.SurveyID'))
    Rand_options = Column(Boolean, nullable=False)
    survey = relationship('Survey')

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
