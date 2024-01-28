#!/usr/bin/python
""" holds class CustomCategory"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey,String
from sqlalchemy.orm import relationship


class CustomCategory(BaseModel, Base):
    __tablename__ = 'customcategory'
    CategoryID = Column(String(60), primary_key=True)
    CategoryName = Column(String(255))
    UserID = Column(String(60), ForeignKey('User.UserID'))
    user = relationship('User')

    def __init__(self, *args, **kwargs):
        """initializes Amenity"""
        super().__init__(*args, **kwargs)
