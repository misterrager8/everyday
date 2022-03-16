from flask_login import UserMixin
from sqlalchemy import Integer, Column, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from JournalSite import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    date_created = Column(DateTime)
    entries = relationship("Entry", backref="users", lazy="dynamic")
    books = relationship("Book", backref="users", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_entries(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.entries.filter(text(filter_)).order_by(text(order_by))

    def get_unsorted(self):
        return self.get_entries(filter_="book is null")

    def get_books(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.books.filter(text(filter_)).order_by(text(order_by))


class Book(db.Model):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    color = Column(Text)
    date_created = Column(DateTime)
    entries = relationship("Entry", backref="books", lazy="dynamic")
    user = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)

    def get_entries(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.entries.filter(text(filter_)).order_by(text(order_by))


class Entry(db.Model):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    date_created = Column(DateTime)
    book = Column(Integer, ForeignKey("books.id"))
    user = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
