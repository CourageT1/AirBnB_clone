#!/usr/bin/python3
""" class BaseModel """
from uuid import uuid4
from datetime import datetime
import models


class BaseModel:
    def __init__(self, *args, **kwargs):
        """
        Constructor for BaseModel.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    continue
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.strptime(value))
                else:
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at

    def save(self):
        """
        Update the 'updated_at' attribute with the current datetime.
        """
        self.updated_at = datetime.now()

    def to_dict(self):
        """
        Convert the instance attributes to a dictionary representation.

        Returns:
            dict: A dictionary containing the instance attributes.
        """
        instance_dict = self.__dict__.copy()
        instance_dict['__class__'] = self.__class__.__name__
        instance_dict['created_at'] = self.created_at.isoformat()
        instance_dict['updated_at'] = self.updated_at.isoformat()
        return instance_dict

    def __str__(self):
        """
        Get a human-readable string representation of the instance.

        Returns:
            str: A formatted string representing the instance.
        """
        return "[{}] ({}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)
