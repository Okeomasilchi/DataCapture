#!/usr/bin/python
""" holds class Question"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, JSON, String, Text, Boolean
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    __tablename__ = 'questions'
    QuestionID = Column(String(60), primary_key=True)
    QuestionText = Column(Text)
    Options = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('surveys.SurveyID'))
    Rand_options = Column(Boolean, nullable=False)
    survey = relationship('Survey', back_populates='questions', cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """initializes city"""
        super().__init__(*args, **kwargs)
