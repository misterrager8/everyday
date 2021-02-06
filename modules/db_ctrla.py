import os

import MySQLdb
from dotenv import load_dotenv

from modules.objects import Post, Blogger


class DB:
    def __init__(self):
        load_dotenv()
        create_table_stmt = "CREATE TABLE IF NOT EXISTS posts(" \
                            "post_id INT AUTO_INCREMENT," \
                            "author TEXT NOT NULL," \
                            "title TEXT NOT NULL," \
                            "content TEXT NOT NULL," \
                            "date_posted TEXT NOT NULL," \
                            "is_public TEXT NOT NULL," \
                            "likes TEXT NOT NULL," \
                            "category TEXT NOT NULL" \
                            "PRIMARY KEY (project_id));"
        self.db_write(create_table_stmt)

    @staticmethod
    def db_read(stmt: str) -> list:
        db = MySQLdb.connect(os.getenv("host"),
                             os.getenv("user"),
                             os.getenv("passwd"),
                             os.getenv("db"))
        cursor = db.cursor()
        try:
            cursor.execute(stmt)
            return cursor.fetchall()
        except MySQLdb.Error as e:
            print(e)

    @staticmethod
    def db_write(stmt: str):
        db = MySQLdb.connect(os.getenv("host"),
                             os.getenv("user"),
                             os.getenv("passwd"),
                             os.getenv("db"))
        cursor = db.cursor()
        try:
            cursor.execute(stmt)
            db.commit()
        except MySQLdb.Error as e:
            print(e)


class PostDB(DB):
    def __init__(self):
        super().__init__()
        init_statement = "CREATE TABLE IF NOT EXISTS posts() VALUES()"
        self.db_write(init_statement)

    def create(self, new_post: Post):
        stmt = "INSERT INTO posts () VALUES ()" % new_post
        self.db_write(stmt)
        print("Added.")

    def read(self) -> list:
        stmt = "SELECT * FROM posts"
        self.db_read(stmt)
        return []

    def update(self, post_id: int):
        stmt = "UPDATE posts SET - = - WHERE post_id = '%d'" % post_id
        self.db_write(stmt)
        print("Updated.")

    def delete(self, post_id: int):
        stmt = "DELETE FROM posts WHERE post_id = '%d'" % post_id
        self.db_write(stmt)
        print("Deleted.")


class BloggerDB(DB):
    def __init__(self):
        super().__init__()
        init_statement = "CREATE TABLE IF NOT EXISTS bloggers() VALUES()"
        self.db_write(init_statement)

    def create(self, new_blogger: Blogger):
        stmt = "INSERT INTO bloggers () VALUES ()" % new_blogger
        self.db_write(stmt)
        print("Added.")

    def read(self) -> list:
        stmt = "SELECT * FROM bloggers"
        self.db_read(stmt)
        return []

    def update(self, blogger_id: int):
        stmt = "UPDATE bloggers SET - = - WHERE blogger_id = '%d'" % blogger_id
        self.db_write(stmt)
        print("Updated.")

    def delete(self, blogger_id: int):
        stmt = "DELETE FROM bloggers WHERE blogger_id = '%d'" % blogger_id
        self.db_write(stmt)
        print("Deleted.")
