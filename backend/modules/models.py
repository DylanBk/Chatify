import datetime
import os
from sqlalchemy import Boolean, Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import time
import uuid

base = declarative_base()

class User(base):
    """
    User class to store user data.
    """
    __tablename__ = "Users"

    id = Column(String, primary_key=True, unique=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String, default="User")
    pfp = Column(String)
    active = Column(Boolean) # 0 = offline, 1 = online
    status = Column(String)
    theme = Column(String, ForeignKey('Themes.id'))

    rel_user_theme = relationship("Theme", back_populates="rel_theme_user")
    rel_user_messages = relationship("Message", back_populates="rel_message_sender")

    def __init__(self, email:str, username:str, password:bytes, role=None):
        """
        Constructor for the User class.
        Parameters:
            email: the user's email
            username: the user's username
            password: the user's password
            role: the user's role - optional
        """
        self.id = str(uuid.uuid4())
        self.username = username
        self.email = email
        self.password = password

        pfp_path = os.path.join(os.path.dirname(__file__), '../media/account.webp')
        with open(pfp_path, 'rb') as f:
            self.pfp = f.read()

        if role: # accounts with permissions can be directly created
            self.role = role # by passing in the appropriate role

class UserRelationship(base):
    """
    UserRelationship class to store user relationships.
    """
    __tablename__ = "UserRelationships"

    id = Column(String, primary_key=True, unique=True)
    id_1 = Column(String, ForeignKey('Users.id'))
    id_2 = Column(String, ForeignKey('Users.id'))
    status = Column(Integer)
    # 0 = friends
    # 1 = user1 to user2 pending
    # 2 = user2 to user1 pending
    # 3 = user1 blocked user2
    # 4 = user2 blocked user1
    # 5 = both blocked both
    # 6 = removed -> delete row

    def __init__(self, id_1, id_2, status):
        """
        Constructor for the UserRelationship class.
        Parameters:
            id_1: the first user's id
            id_2: the second user's id
            status: the relationship status
        """
        self.id = f"ur/{id_1}/{id_2}"
        self.id_1 = id_1
        self.id_2 = id_2
        self.status = status

class Chat(base):
    __tablename__ = "Chats"

    id = Column(String, primary_key=True, unique=True)
    id_1 = Column(String, ForeignKey('Users.id'))
    id_2 = Column(String, ForeignKey('Users.id'))

    rel_chat_messages = relationship("Message", back_populates="rel_message_chat")

    def __init__(self, id_1, id_2):
        self.id = f"ch/{id_1}/{id_2}"
        self.id_1 = id_1
        self.id_2 = id_2

class Message(base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sender_id = Column(String, ForeignKey('Users.id'))
    sender_username = Column(String)
    chat = Column(String, ForeignKey('Chats.id'))
    content = Column(String)
    timestamp = Column(String, default=datetime.datetime.utcnow)

    rel_message_sender = relationship("User", back_populates="rel_user_messages")
    rel_message_chat = relationship("Chat", back_populates="rel_chat_messages")

    def __init__(self, sender_id, sender_username, chat, content, timestamp):
        print('\n', sender_id, sender_username, chat, content, timestamp, '\n')
        self.sender_id = sender_id
        self.sender_username = sender_username
        self.chat = chat
        self.content = content
        self.timestamp = timestamp

class Theme(base):
    __tablename__ = "Themes"

    id = Column(String, primary_key=True, unique=True)
    name = Column(String, default="Default: Light")
    background = Column(String)
    foreground = Column(String)
    primary = Column(String)
    secondary = Column(String)
    danger = Column(String)

    rel_theme_user = relationship("User", back_populates="rel_user_theme")

    def __init__(self, name, background, foreground, primary, secondary, danger):
        unix = time.time()
        self.id = f"th/{name}/{unix}"
        self.name = name
        self.background = background
        self.foreground = foreground
        self.primary = primary
        self.secondary = secondary
        self.danger = danger