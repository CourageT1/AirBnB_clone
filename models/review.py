#!/usr/bin/python3
""" class Review """
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review class which inherit BaseModel """
    place_id = ""
    user_id = ""
    text = "
