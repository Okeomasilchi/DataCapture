#!/usr/bin/python
""" holds class Survey"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, Text, Date, Boolean, Index
from sqlalchemy.orm import relationship


class Survey(BaseModel, Base):
    """
    Represents a survey.

    Attributes:
        user_id (str): The ID of the user who created the survey.
        title (str): The title of the survey.
        description (str): The description of the survey.
        expiry_date (datetime.date): The expiry date of the survey.
        visibility (bool): The visibility status of the survey.
        randomize (bool): The randomization status of the survey.
        question_type (str): The type of questions in the survey.
        user (User): The user who created the survey.
        questions (List[Question]): The list of questions in the survey.
        responses (List[Response]): The list of responses to the survey.
    """

    __tablename__ = 'surveys'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    expiry_date = Column(Date)
    visibility = Column(Boolean, nullable=False)
    randomize = Column(Boolean, nullable=False)
    question_type = Column(String(120), nullable=False)
    user = relationship('User', cascade="all, delete-orphan")
    questions = relationship('Question', back_populates='survey',
                             cascade="all, delete-orphan"
                             )
    responses = relationship('Response', back_populates='survey',
                             cascade="all, delete-orphan"
                             )

    __table_args__ = (
            Index('idx_survey_id', 'id'),
        )

    def __init__(self, *args, **kwargs):
        """initializes Survey"""
        super().__init__(*args, **kwargs)
