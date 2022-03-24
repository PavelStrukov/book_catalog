from enum import Enum


class Type(Enum):
    """Class for storing the type of the book in catalog"""
    SCIENCE_FICTION = "Science fiction"
    SATIRE = "Satire"
    DRAMA = "Drama"
    ACTION_AND_ADVENTURE = "Action and adventure"
    ROMANCE = "Romance"
