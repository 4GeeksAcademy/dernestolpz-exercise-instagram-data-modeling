import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    username = Column(String(250), unique=True, nullable=False)
    email = Column(String(250), unique=True, nullable=False)
    password = Column(String(250), nullable=False)

    
    posts = relationship("Post", backref="author", lazy="dynamic")
    comments = relationship("Comment", backref="author", lazy="dynamic")
    followers = relationship("Follower", backref="follower", lazy="dynamic")
    following = relationship("Follower", backref="user", lazy="dynamic")


class Follower(Base):
    __tablename__ = 'followers'
    id = Column(Integer, primary_key=True)
    accepted = Column(Boolean, default=False)

    follower_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    image_url = Column(String(500), nullable=False)
    description = Column(String(250))

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="posts")

    
    likes = relationship("Like", backref="post", lazy="dynamic")
    comments = relationship("Comment", backref="post", lazy="dynamic")


class Like(Base):
    __tablename__ = 'likes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


class Media(Base):
    __tablename__ = 'media'
    id = Column(Integer, primary_key=True)
    url = Column(String(500), nullable=False)
    media_type = Column(String(50), nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", backref="media", lazy="dynamic")


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    text = Column(String(250))

    user_id = Column(Integer, ForeignKey('users.id'))
    post_id = Column(Integer, ForeignKey('posts.id'))


engine = create_engine('sqlite:///instagram_clone.db')
Base.metadata.create_all(engine)


try:
    render_er(Base, 'diagram.png')
    print("Success! The ER diagram has been generated as diagram.png.")
except Exception as e:
    print("There was a problem generating the diagram.")
    raise e
