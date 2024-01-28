#!/usr/bin/python
""" holds class CustomCategory"""
from models.base_model import BaseModel, Base
from models.user import User
from sqlalchemy import Column, ForeignKey,String, VARCHAR, Index
from sqlalchemy.orm import relationship


class CustomCategory(BaseModel, Base):
    __tablename__ = 'customcategory'

    CategoryID = Column(String(60), primary_key=True)
    CategoryName = Column(String(255))
    UserID = Column(VARCHAR(60), ForeignKey('users.UserID'))  # Fix the foreign key reference
    user = relationship('User')

    __table_args__ = (
        Index('idx_category_id', 'CategoryID'),
    )
    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
