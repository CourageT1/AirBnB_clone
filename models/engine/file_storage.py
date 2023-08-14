#!/usr/bin/python3

"""class FileStorage
    serialize instance to JSON file
    and deserialize JSON file to instance"""
import json
import uuid
import os
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
    This class handles JSON serialization and deserialization of instances.
    """

    __file_path = "file.json"
    __objects = {}

    def __init__(self):
        """
        Initializes the FileStorage instance.
        """
        self.reload()

    def all(self):
        """
        Returns the dictionary __objects.
        """
        return FileStorage.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        obj_dict = {key: obj.to_dict() for key, obj in FileStorage.__objects.items()}
        with open(FileStorage.__file_path, "w") as file:
            json.dump(obj_dict, file)

    def reload(self):
        """
        Deserializes the JSON file to __objects (if the file exists).
        """
        if os.path.exists(FileStorage.__file_path):
            with open(FileStorage.__file_path, "r") as file:
                obj_dict = json.load(file)
                for key, value in obj_dict.items():
                    cls_name = value["__class__"]
                    cls = eval(cls_name)
                    obj = cls(**value)
                    FileStorage.__objects[key] = obj
