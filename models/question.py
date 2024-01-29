#!/usr/bin/python
""" holds class Question"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, JSON, String, Text, Boolean
from sqlalchemy.orm import relationship


class Question(BaseModel, Base):
    """
    Represents a question in a survey.

    Attributes:
        question (str): The text of the question.
        options (list): The options for the question (if applicable).
        survey_id (str): The ID of the survey the question belongs to.
        random (bool): Indicates whether the question should be
                        displayed in a random order.
        survey (Survey): The survey object that the question belongs to.

    """
    __tablename__ = 'questions'

    question = Column(Text, nullable=False)
    options = Column(JSON)
    survey_id = Column(String(60), ForeignKey('surveys.id'), nullable=False)
    random = Column(Boolean, nullable=False)
    survey = relationship('Survey', back_populates='questions',
                          cascade="all, delete-orphan"
                          )

    def __init__(self, *args, **kwargs):
        """Initializes a new instance of the Question class."""
        super().__init__(*args, **kwargs)
