#!/usr/bin/python
""" holds class Response"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, DateTime, JSON
from sqlalchemy.orm import relationship
import datetime


class Response(BaseModel, Base):
    """
    Represents a response to a survey.

    Attributes:
        bio (dict): The bio information of the respondent.
        timestamp (datetime): The timestamp of the response.
        answers (dict): The answers provided by the respondent.
        survey_id (str): The ID of the survey the response belongs to.
        survey (Survey): The survey object associated with the response.
    """

    __tablename__ = "responses"

    bio = Column(JSON)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow())
    answers = Column(JSON, nullable=False)
    survey_id = Column(String(60), ForeignKey("surveys.id"), nullable=False)
    survey = relationship("Survey", back_populates="responses")

    def __init__(self, *args, **kwargs):
        """Initializes a Response object."""
        super().__init__(*args, **kwargs)
