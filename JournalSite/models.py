import datetime

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
    entries = relationship("Entry", backref="user", lazy="dynamic")

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return self.username


class Entry(db.Model):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    date_created = Column(DateTime)
    user = Column(Integer, ForeignKey("users.id"))

    def __init__(self, **kwargs):
        super(Entry, self).__init__(**kwargs)

    def __str__(self):
        return self


class Database:
    def __init__(self):
        pass

    @staticmethod
    def create(object_):
        db.session.add(object_)
        db.session.commit()

    @staticmethod
    def read(type_, id_: int):
        return db.session.query(type_).get(id_)

    @staticmethod
    def update(object_, **kwargs):
        for key, value in kwargs.items():
            object_.key = value
        db.session.commit()

    @staticmethod
    def delete(object_):
        db.session.delete(object_)
        db.session.commit()

    @staticmethod
    def search(type_, order_by: str, filter_: str):
        return db.session.query(type_).order_by(text(order_by)).filter(text(filter_)).all()

    @staticmethod
    def execute_stmt(stmt: str):
        db.session.execute(stmt)
        db.session.commit()


class Calendar:
    def __init__(self):
        pass

    @staticmethod
    def get_week(day: datetime.date) -> list:
        return [day - datetime.timedelta(days=i) for i in range(0, 7)]

    @staticmethod
    def get_month(day: datetime.date) -> list:
        return [day - datetime.timedelta(days=i) for i in range(0, 30)]

    @staticmethod
    def get_year(day: datetime.date) -> list:
        return [day - datetime.timedelta(days=i) for i in range(0, 365)]
