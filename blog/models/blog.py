"""
Blog model for blog posts
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from blog.models.user import User
    from blog.models.comment import Comment

class Blog(SQLModel, table=True):
    """
    Blog post database model
    Each blog belongs to a user and can have multiple comments
    """
    __tablename__ = "blogs"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Blog Content
    title: str = Field(index=True, nullable=False)
    body: str = Field(nullable=False)
    published: bool = Field(default=True)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Foreign Key
    creator_id: int = Field(foreign_key="users.id", nullable=False)
    
    # Relationships - Use string quotes for forward references
    creator: Optional["User"] = Relationship(back_populates="blogs")
    comments: List["Comment"] = Relationship(
        back_populates="blog",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
