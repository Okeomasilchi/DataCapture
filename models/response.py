#!/usr/bin/python
""" holds class Response"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class Response(BaseModel, Base):
    __tablename__ = 'response'
    ResponseID = Column(String(60), primary_key=True)
    responders_bio = Column(JSON)
    Timestamp = Column(DateTime)
    Answers = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('surveys.SurveyID'))
    survey = relationship('Survey', back_populates='responses', cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Place"""
        super().__init__(*args, **kwargs)
