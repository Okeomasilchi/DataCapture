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

CREATE TABLE `CustomCategory`
(
 `CategoryID`   varchar(60) NOT NULL ,
 `CategoryName` varchar(255) NULL ,
 `UserID`       varchar(60) NULL ,

PRIMARY KEY (`CategoryID`),
KEY `UserID` (`UserID`),
CONSTRAINT `UserID` FOREIGN KEY `UserID` (`UserID`) REFERENCES `User` (`UserID`)
);


CREATE TABLE `Question`
(
 `QuestionID`   varchar(60) NOT NULL ,
 `QuestionText` text NULL ,
 `Options`      json NULL ,
 `SurveyID`     varchar(60) NULL ,
 `Rand_options` bool NOT NULL ,

PRIMARY KEY (`QuestionID`),
KEY `SurveyID` (`SurveyID`),
CONSTRAINT `SurveyID` FOREIGN KEY `SurveyID` (`SurveyID`) REFERENCES `Survey` (`SurveyID`)
);

CREATE TABLE `Response`
(
 `ResponseID` varchar(60) NOT NULL ,
 `Timestamp`  timestamp NULL ,
 `Answers`    json NULL ,
 `SurveyID`   varchar(60) NULL ,

PRIMARY KEY (`ResponseID`),
KEY `SurveyID` (`SurveyID`),
CONSTRAINT `SurveyID` FOREIGN KEY `SurveyID` (`SurveyID`) REFERENCES `Survey` (`SurveyID`)
);

CREATE TABLE `Survey`
(
 `SurveyID`      varchar(60) NOT NULL ,
 `user_id`       varchar(60) NOT NULL ,
 `Title`         varchar(255) NOT NULL ,
 `Description`   text NOT NULL ,
 `created_at`    datetime NOT NULL ,
 `ExpiryDate`    date NULL ,
 `Visibility`    bool NOT NULL ,
 `Randomise`     bool NOT NULL ,
 `QuestionsType` varchar(120) NOT NULL ,
 `updated_at`    datetime NOT NULL ,

PRIMARY KEY (`SurveyID`),
KEY `CreatorID` (`user_id`),
CONSTRAINT `CreatorID` FOREIGN KEY `CreatorID` (`user_id`) REFERENCES `User` (`UserID`)
);

CREATE TABLE `SurveyCategory`
(
 `SurveyCategoryID` varchar(60) NOT NULL ,
 `SurveyID`         varchar(60) NULL ,
 `CategoryID`       varchar(60) NULL ,

PRIMARY KEY (`SurveyCategoryID`),
KEY `CategoryID` (`CategoryID`),
CONSTRAINT `CategoryID` FOREIGN KEY `CategoryID` (`CategoryID`) REFERENCES `CustomCategory` (`CategoryID`),
KEY `SurveyID` (`SurveyID`),
CONSTRAINT `SurveyID` FOREIGN KEY `SurveyID` (`SurveyID`) REFERENCES `Survey` (`SurveyID`)
);

CREATE TABLE `User`
(
 `UserID`    varchar(60) NOT NULL ,
 `FirstName` varchar(255) NOT NULL ,
 `Email`     varchar(255) NOT NULL ,
 `Password`  varchar(255) NOT NULL ,
 `lastName`  varchar(255) NULL ,

PRIMARY KEY (`UserID`)
);