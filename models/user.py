#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy import Column, VARCHAR, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'
    UserID = Column(VARCHAR(60), primary_key=True)
    FirstName = Column(String(255))
    Email = Column(String(255), unique=True)
    Password = Column(VARCHAR(255))
    LastName = Column(String(255))

    user_surveys = relationship('Survey', backref='user',
                                lazy=True, cascade="all, delete-orphan"
                                )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
