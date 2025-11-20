"""
Comment model for blog comments
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from blog.models.blog import Blog
    from blog.models.user import User

class Comment(SQLModel, table=True):
    """
    Comment database model
    Each comment belongs to a blog and a user (author)
    Many-to-one relationship with both Blog and User
    """
    __tablename__ = "comments"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Comment Content
    content: str = Field(nullable=False)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Keys
    blog_id: int = Field(foreign_key="blogs.id", nullable=False)
    author_id: int = Field(foreign_key="users.id", nullable=False)
    
    # Relationships - Use string quotes for forward references
    blog: Optional["Blog"] = Relationship(back_populates="comments")
    author: Optional["User"] = Relationship(back_populates="comments")
