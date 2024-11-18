from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class UserDB(db.Model):
    id : Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(200))

    files: Mapped[List["FileDB"]] = relationship(back_populates="")
    
    def __init__(self, username = None, password = None, name = None, description = None, id = None):
        if id is not None:
            self.id = id
        self.username = username
        self.password = password
        self.name = name
        self.description = description

    def toJson(self):
        return {
            "id": self.id,
            "username": self.username, 
            "name": self.name,
            "description": self.description
        }
    
    def toToken(self):
        return {
            "id": self.id,
            "username": self.username,
            "name": self.name
        }
    
    def __repr__(self):
        return f"User {self.username}"

class FileDB(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    url: Mapped[str] = mapped_column(String(150), nullable=False)
    userId: Mapped[int] = mapped_column(ForeignKey("user_db.id"))

    user: Mapped["UserDB"] = relationship(back_populates="files")

    def __init__(self, name=None, url=None, userId=None):
        self.name = name
        self.url = url
        self.userId = userId

    def __repr__(self):
        return f"File: {self.name} by {self.userId}:{self.user.name}"
    
    def toJson(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "userId": self.userId,
            "user_name": self.user.name
        }

class BlacklistTokens(db.Model):
    token: Mapped[str] = mapped_column(String(255), primary_key=True)

    def __init__(self, token):
        self.token = token