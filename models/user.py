#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, VARCHAR, String, Index
from sqlalchemy.orm import relationship

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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
