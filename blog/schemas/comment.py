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

class CommentUpdate(BaseModel):
    """Schema for updating a comment"""
    content: str

class CommentResponse(CommentBase):
    """Schema for comment response"""
    id: int
    blog_id: int
    created_at: datetime
    updated_at: datetime
    author: UserInBlog
    
    class Config:
        from_attributes = True
