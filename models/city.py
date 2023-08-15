#!/usr/bin/python3
""" class City """
from models.base_model import BaseModel


class City(BaseModel):
    """ City class which inherit BaseModel """
    state_id = ""
    name = ""
