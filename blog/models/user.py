"""
User model for authentication and profile management
"""
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from blog.models.blog import Blog
    from blog.models.comment import Comment

class AuthProvider(str, Enum):
    """Authentication provider enumeration"""
    EMAIL = "email"
    GOOGLE = "google"

class User(SQLModel, table=True):
    """
    User database model
    Supports both email/password and Google OAuth authentication
    """
    __tablename__ = "users"
    
    # Primary Key
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Basic Info - ONLY THESE FIELDS
    email: str = Field(unique=True, index=True, nullable=False)
    full_name: str = Field(nullable=False)
    hashed_password: Optional[str] = Field(default=None)  # Nullable for OAuth users
    
    # Google OAuth fields
    google_id: Optional[str] = Field(default=None, unique=True, index=True)
    google_email: Optional[str] = Field(default=None)
    auth_provider: AuthProvider = Field(default=AuthProvider.EMAIL)
    
    # Account status
    is_verified: bool = Field(default=False)
    is_active: bool = Field(default=True)
    
    # Relationships
    blogs: List["Blog"] = Relationship(back_populates="creator")
    comments: List["Comment"] = Relationship(back_populates="author")
