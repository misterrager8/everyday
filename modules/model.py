import datetime

from sqlalchemy import Column, Text, Integer


class Post:
    __tablename__ = "posts"

    title = Column(Text)
    content = Column(Text)
    date_posted = Column(Text)
    id = Column(Integer, primary_key=True)

    def __init__(self,
                 title: str,
                 content: str,
                 date_posted: str = datetime.datetime.now().strftime("%Y-%m-%d")):
        self.title = title
        self.content = content
        self.date_posted = date_posted

    def insert(self): pass

    def update(self): pass

    def delete(self): pass

    def to_string(self):
        print(self.title, "\t", self.date_posted)
