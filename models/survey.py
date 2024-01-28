#!/usr/bin/python
""" holds class Survey"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Text, DateTime, Date, Boolean
from sqlalchemy.orm import relationship


class Survey(BaseModel, Base):
    __tablename__ = 'surveys'
    SurveyID = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('users.UserID'))
    Title = Column(String(255))
    Description = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    ExpiryDate = Column(Date)
    Visibility = Column(Boolean)
    Randomize = Column(Boolean)
    QuestionsType = Column(String(120))
    user = relationship('User', cascade="all, delete-orphan")
    questions = relationship('Question', back_populates='survey', cascade="all, delete-orphan")
    responses = relationship('Response', back_populates='survey', cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes Review"""
        super().__init__(*args, **kwargs)
