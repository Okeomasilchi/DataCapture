#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.customcategory import CustomCategory
from models.base_model import BaseModel, Base
from models.question import Question
from models.response import Response
from models.survey import Survey
from models.surveycategory import SurveyCategory
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "CustomCategory": CustomCategory,
    "Question": Question,
    "Response": Response,
    "Survey": Survey,
    "SurveyCategory": SurveyCategory,
    "User": User
    }


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        DC_MYSQL_USER = getenv('DC_MYSQL_USER')
        DC_MYSQL_PWD = getenv('DC_MYSQL_PWD')
        DC_MYSQL_HOST = getenv('DC_MYSQL_HOST')
        DC_MYSQL_DB = getenv('DC_MYSQL_DB')
        DC_ENV = getenv('DC_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(DC_MYSQL_USER,
                                             DC_MYSQL_PWD,
                                             DC_MYSQL_HOST,
                                             DC_MYSQL_DB))
        if DC_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj

        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.close()

    def get(self, cls, id):
        """
        Retrieves an instance of a class by its
        ID from a collection of instances.

        Args:
          cls: class of objects that you want to retrieve.
          id: unique identifier of the instance to retrieve.

        Returns:
          The instance with the specified id is being
          returned.
        """
        instances = self.all(cls)
        ins = instances.pop("{}.{}".
                            format(cls.__name__, id), None)
        return ins

    def count(self, cls=None):
        """
        Counts the number of objects in a given
        class or all classes if no class is
        specified.

        Args:
          cls: Optional argument that represents a class.

        Returns:
          Returns the length of all classes if no cls
          else returns length of the cls classes
        """
        if cls:
            return len(self.all(cls))
        return len(self.all())
