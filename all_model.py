from sqlalchemy import Column, ForeignKey, String, Index, Text, DateTime, Date, Boolean, JSON, VARCHAR
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from models.base_model import BaseModel


Base = declarative_base()


class CustomCategory(BaseModel, Base):
    __tablename__ = 'customcategory'

    CategoryID = Column(String(60), primary_key=True)
    CategoryName = Column(String(255))
    UserID = Column(VARCHAR(60), ForeignKey('users.UserID'))  # Fix the foreign key reference
    user = relationship('User')

    __table_args__ = (
        Index('idx_category_id', 'CategoryID'),
    )

class Question(BaseModel, Base):
    __tablename__ = 'questions'
    QuestionID = Column(String(60), primary_key=True)
    QuestionText = Column(Text)
    Options = Column(JSON)
    survey_id = Column(String(60), ForeignKey('surveys.SurveyID'))
    Rand_options = Column(Boolean, nullable=False)
    survey = relationship('Survey', back_populates='questions', cascade="all, delete-orphan")


class Response(BaseModel, Base):
    __tablename__ = 'response'
    ResponseID = Column(String(60), primary_key=True)
    responders_bio = Column(JSON)
    Timestamp = Column(DateTime)
    Answers = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('surveys.SurveyID'))
    survey = relationship('Survey', back_populates='responses', cascade="all, delete-orphan")


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

    __table_args__ = (
            Index('idx_survey_id', 'SurveyID'),
        )


class SurveyCategory(BaseModel, Base):
    __tablename__ = 'surveycategory'

    SurveyCategoryID = Column(String(60), primary_key=True)
    SurveyID = Column(String(60), ForeignKey('surveys.SurveyID'))
    category_id = Column(String(60), ForeignKey('customcategory.CategoryID'))
    survey = relationship('Survey')
    category = relationship('CustomCategory')


class User(BaseModel, Base):
    __tablename__ = 'users'
    UserID = Column(VARCHAR(60), primary_key=True)
    FirstName = Column(String(255))
    Email = Column(String(255), unique=True)
    Password = Column(VARCHAR(255))
    LastName = Column(String(255))

    user_surveys = relationship('Survey', backref='user',
                                lazy=True, cascade="all, delete-orphan"
                                )

    __table_args__ = (
        Index('idx_user_id', 'UserID'),
    )
