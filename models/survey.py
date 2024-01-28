#!/usr/bin/python
""" holds class Review"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Survey(BaseModel, Base):
    __tablename__ = 'Survey'
    SurveyID = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('User.UserID'))
    Title = Column(String(255))
    Description = Column(Text)
    created_at = Column(DateTime)
    ExpiryDate = Column(Date)
    Visibility = Column(Boolean)
    Randomize = Column(Boolean)
    QuestionsType = Column(String(120))
    updated_at = Column(DateTime)
    user = relationship('User')

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
