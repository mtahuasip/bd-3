from datetime import datetime
from bson.objectid import ObjectId


class Post:
    def __init__(self, title, content, username):
        self.title = title
        self.content = content
        self.username = username
        self.comments = []
        self.createdAt = datetime.now()
        self.updatedAt = self.createdAt

    def to_collection(self):
        return {
            "title": self.title,
            "content": self.content,
            "username": self.username,
            "comments": self.comments,
            "createdAt": self.createdAt,
            "updatedAt": self.updatedAt,
        }
