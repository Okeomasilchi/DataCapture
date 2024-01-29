#!/usr/bin/python3
""" holds class User"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, VARCHAR, String, Index
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Represents a user in the system.
    """

    __tablename__ = 'users'

    first_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(VARCHAR(255), nullable=False)
    last_name = Column(String(255), nullable=False)

    user_surveys = relationship('Survey', backref='user',
                                lazy=True, cascade="all, delete-orphan"
                                )

    __table_args__ = (
            Index('idx_user_id', 'id'),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
