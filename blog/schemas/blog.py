"""
Blog schemas for request/response validation
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from blog.schemas.user import UserInBlog

class BlogBase(BaseModel):
    """Base blog schema"""
    title: str
    body: str
    published: bool = True

class BlogCreate(BlogBase):
    """Schema for creating a blog"""
    pass

class BlogUpdate(BaseModel):
    """Schema for updating a blog"""
    title: Optional[str] = None
    body: Optional[str] = None
    published: Optional[bool] = None

class CommentInBlog(BaseModel):
    """Minimal comment info for blog responses"""
    id: int
    content: str
    author_id: int
    created_at: datetime
    author: Optional[UserInBlog] = None
    
    class Config:
        from_attributes = True

class BlogResponse(BlogBase):
    """Schema for blog response"""
    id: int
    creator_id: int
    created_at: datetime
    updated_at: datetime
    creator: Optional[UserInBlog] = None
    comments: List[CommentInBlog] = []
    
    class Config:
        from_attributes = True
