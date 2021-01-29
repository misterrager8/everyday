class Blogger:
    def __init__(self,
                 username: str,
                 date_created: str,
                 email: str = None,
                 location: str = None,
                 blogger_id: int = None):
        self.username = username
        self.date_created = date_created
        self.email = email
        self.location = location
        self.blogger_id = blogger_id

    def to_string(self):
        print(self.blogger_id,
              self.username,
              self.date_created,
              self.email,
              self.location)


class Post:
    def __init__(self,
                 author: str,
                 title: str,
                 content: str,
                 date_posted: str,
                 is_public: bool = False,
                 likes: int = None,
                 category: str = None,
                 post_id: int = None):
        self.author = author
        self.title = title
        self.content = content
        self.date_posted = date_posted
        self.is_public = is_public
        self.likes = likes
        self.category = category
        self.post_id = post_id

    def to_string(self):
        print(self.post_id,
              self.author,
              self.title,
              self.content,
              self.date_posted,
              self.is_public,
              self.likes,
              self.category)
