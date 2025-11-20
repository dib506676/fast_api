"""
Comment schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from blog.schemas.user import UserInBlog

class CommentBase(BaseModel):
    """Base comment schema"""
    content: str

class CommentCreate(CommentBase):
    """Schema for creating a comment"""
    blog_id: int

class CommentUpdate(CommentBase):
    """Schema for updating a comment"""
    pass

class CommentResponse(CommentBase):
    """Schema for comment response"""
    id: int
    blog_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    author: Optional[UserInBlog] = None  # Include author info
    
    class Config:
        from_attributes = True
