# from typing import Optional, List
# from sqlmodel import SQLModel, Field, Relationship

# class User(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     name: str
#     email: str
#     hashed_password: str
#     blogs: List["Blog"] = Relationship(back_populates="creator")
#     comments: List["Comment"] = Relationship(back_populates="author")

# class Blog(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     title: str
#     content: str
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     creator: Optional[User] = Relationship(back_populates="blogs")
#     comments: List["Comment"] = Relationship(back_populates="blog")

# class Comment(SQLModel, table=True):
#     id: Optional[int] = Field(default=None, primary_key=True)
#     content: str
#     blog_id: Optional[int] = Field(default=None, foreign_key="blog.id")
#     user_id: Optional[int] = Field(default=None, foreign_key="user.id")
#     blog: Optional[Blog] = Relationship(back_populates="comments")
#     author: Optional[User] = Relationship(back_populates="comments")
