from flask_login import UserMixin
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from moodJournal import db


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(Text)
    password = Column(Text)
    date_created = Column(DateTime)
    entries = relationship("Entry", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_entries(self, filter_: str = "", order_by: str = "date_created desc"):
        return self.entries.filter(text(filter_)).order_by(text(order_by))


class Entry(db.Model):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    mood = Column(Text)
    content = Column(Text)
    date_created = Column(DateTime)
    user = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)
