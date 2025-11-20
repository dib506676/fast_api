"""
Authentication schemas for login and tokens
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from blog.schemas.user import UserResponse

class LoginRequest(BaseModel):
    """Schema for login request"""
    email: EmailStr
    password: str

class Token(BaseModel):
    """Schema for token response"""
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    """Schema for decoded token data"""
    user_id: Optional[int] = None

class GoogleAuthRequest(BaseModel):
    """Schema for Google OAuth request"""
    id_token: str
