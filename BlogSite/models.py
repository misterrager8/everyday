from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Text, Integer, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from BlogSite import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    username = Column(Text)
    password = Column(Text)
    date_created = Column(Date, default=datetime.today())
    posts = relationship("Post", backref="User")
    bookmarks = relationship("Post", secondary="user_bookmark_assocs")
    id = Column(Integer, primary_key=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def __str__(self):
        return "%d\t%s" % (self.id, self.username)


class Post(db.Model):
    __tablename__ = "posts"

    title = Column(Text)
    content = Column(Text)
    visible = Column(Boolean)
    date_created = Column(DateTime, default=datetime.now())
    author = Column(Integer, ForeignKey("users.id"))
    id = Column(Integer, primary_key=True)

    def in_favs(self, user_id: int) -> bool:
        _ = db.session.query(User).get(user_id)
        return self in _.bookmarks

    def __str__(self):
        return "%d\t%s" % (self.id, self.title)


class Assoc(db.Model):
    __tablename__ = "user_bookmark_assocs"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"), primary_key=True)


db.create_all()
