#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'user'
    UserID = Column(String(60), primary_key=True)
    FirstName = Column(String(255))
    Email = Column(String(255))
    Password = Column(String(255))
    lastName = Column(String(255))

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
