from datetime import date

from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from BlogSite import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    date_created = Column(Date)
    posts = relationship("Post", backref="User")
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 username: str,
                 password: str,
                 date_created: date = date.today()):
        self.username = username
        self.password = password
        self.date_created = date_created

    def __str__(self):
        return "%d\t%s" % (self.id, self.username)


class Post(db.Model):
    __tablename__ = "posts"

    title = Column(Text)
    content = Column(Text)
    visible = Column(Boolean)
    date_created = Column(DateTime)
    author = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 content: str,
                 visible: bool,
                 date_created: date = date.today()):
        self.title = title
        self.content = content
        self.visible = visible
        self.date_created = date_created

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


db.create_all()
