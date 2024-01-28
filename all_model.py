from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class CustomCategory(Base):
    __tablename__ = 'CustomCategory'
    CategoryID = Column(String(60), primary_key=True)
    CategoryName = Column(String(255))
    UserID = Column(String(60), ForeignKey('User.UserID'))
    user = relationship('User')

class Question(Base):
    __tablename__ = 'Question'
    QuestionID = Column(String(60), primary_key=True)
    QuestionText = Column(Text)
    Options = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('Survey.SurveyID'))
    Rand_options = Column(Boolean, nullable=False)
    survey = relationship('Survey')

class Response(Base):
    __tablename__ = 'Response'
    ResponseID = Column(String(60), primary_key=True)
    Timestamp = Column(DateTime)
    Answers = Column(JSON)
    SurveyID = Column(String(60), ForeignKey('Survey.SurveyID'))
    survey = relationship('Survey')

class Survey(Base):
    __tablename__ = 'Survey'
    SurveyID = Column(String(60), primary_key=True)
    user_id = Column(String(60), ForeignKey('User.UserID'))
    Title = Column(String(255))
    Description = Column(Text)
    created_at = Column(DateTime)
    ExpiryDate = Column(Date)
    Visibility = Column(Boolean)
    Randomise = Column(Boolean)
    QuestionsType = Column(String(120))
    updated_at = Column(DateTime)
    user = relationship('User')

class SurveyCategory(Base):
    __tablename__ = 'SurveyCategory'
    SurveyCategoryID = Column(String(60), primary_key=True)
    SurveyID = Column(String(60), ForeignKey('Survey.SurveyID'))
    CategoryID = Column(String(60), ForeignKey('CustomCategory.CategoryID'))
    survey = relationship('Survey')
    category = relationship('CustomCategory')

class User(Base):
    __tablename__ = 'User'
    UserID = Column(String(60), primary_key=True)
    FirstName = Column(String(255))
    Email = Column(String(255))
    Password = Column(String(255))
    lastName = Column(String(255))
