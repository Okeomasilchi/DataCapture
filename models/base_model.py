#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from json import loads as jl
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""

    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """String representation of the BaseModel class"""
        data = self.__dict__
        if "_sa_instance_state" in data:
            del data["_sa_instance_state"]
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id, data)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()

        if "created_at" in new_dict:
            new_dict["created_at"] = str(new_dict["created_at"])

        if "updated_at" in new_dict:
            new_dict["updated_at"] = str(new_dict["updated_at"])

        if "expiry_date" in new_dict:
            new_dict["expiry_date"] = str(new_dict["expiry_date"])

        new_dict["__class__"] = self.__class__.__name__

        if new_dict["__class__"] == "Question" and "options" in new_dict:
            try:
                new_dict["options"] = jl(new_dict["options"])
            except Exception as e:
                pass

        if new_dict["__class__"] == "Response":
            try:
                new_dict["bio"] = jl(new_dict["bio"])
                new_dict["answers"] = jl(new_dict["answers"])
                new_dict["timestamp"] = str(new_dict["timestamp"])
            except Exception as e:
                pass

        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]

        if getenv("DC_TYPE_STORAGE") == "db":
            new_dict.pop("password", None)

        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
