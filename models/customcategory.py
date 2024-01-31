#!/usr/bin/python
""" holds class CustomCategory"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, ForeignKey, String, VARCHAR, Index
from sqlalchemy.orm import relationship


class CustomCategory(BaseModel, Base):
    """
    Represents a custom category.

    Attributes:
        name (str): The name of the custom category.
        user_id (str): The ID of the user associated with the custom category.
        user (User): The user object associated with the custom category.
    """

    __tablename__ = 'customcategory'

    name = Column(String(255), nullable=False)
    user_id = Column(VARCHAR(60), ForeignKey('users.id'), nullable=False)
    user = relationship('User', cascade="all, delete", single_parent=True)

    __table_args__ = (
        Index('idx_category_id', 'id'),
    )

    def __init__(self, *args, **kwargs):
        """Initializes a CustomCategory object."""
        super().__init__(*args, **kwargs)
