import datetime
from uuid import uuid4

from type import Type


def generate_first_four_books():
    """Function provides generation of the test data"""
    book_1 = Book(Type.DRAMA.value, "THE GREAT GATSBY", "2020-02-03")
    book_2 = Book(Type.ACTION_AND_ADVENTURE.value, "HARRY POTTER", "2020-01-05")
    book_3 = Book(Type.SCIENCE_FICTION.value, "STARS AND PLANETS", "2020-01-01")
    book_4 = Book(Type.SATIRE.value, "THE GREAT GATSBY", "2020-01-20")
    return [book_1, book_2, book_3, book_4]


class Book(object):
    """
    Book class represents the book object with several attributes

        ...

        Attributes
        ----------
        type : Type
            A enum contains a info about type of the book
        title : str
            A string contains a title of the book
            length < 256 symbols
        id : str
            A unique string contains a id of the book
            Generates every time when the book object created
        creation_date : str
            A string contains a creation date and time in YYYY-MM-DD HH:MM:SS format
            Can be null
        updated_date_time : datetime
            A datetime object contains an updating date and time in ISO 860 format"""

    def __init__(self, type, title, creation_date=None):
        self.type = type
        self.title = title[:256]
        self.id = str(uuid4())
        self.creation_date = creation_date + ' 00:00:00'
        self.updated_date_time = datetime.datetime.strptime(self.creation_date, '%Y-%m-%d %H:%M:%S')

    def set_title(self, new_title):
        self.title = new_title
