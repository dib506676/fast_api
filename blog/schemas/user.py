"""
User schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from blog.models.user import AuthProvider

class UserBase(BaseModel):
    """Base user schema with common fields"""
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    """Schema for user registration - Only email, full_name, password"""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user profile"""
    full_name: Optional[str] = None

class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    auth_provider: AuthProvider
    is_verified: bool
    is_active: bool
    
    class Config:
        from_attributes = True

class UserInBlog(BaseModel):
    """Minimal user info for blog/comment responses"""
    id: int
    full_name: str
    email: EmailStr
    
    class Config:
        from_attributes = True
