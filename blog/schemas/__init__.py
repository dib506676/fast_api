"""
Schema exports
"""
from blog.schemas.user import (
    UserBase,
    UserCreate,
    UserUpdate,
    UserResponse,
    UserInBlog
)
from blog.schemas.blog import (
    BlogBase,
    BlogCreate,
    BlogUpdate,
    BlogResponse,  # ← This exists
    CommentInBlog   # ← Add this
)
from blog.schemas.comment import (
    CommentBase,
    CommentCreate,
    CommentUpdate,
    CommentResponse
)
from blog.schemas.auth import (
    LoginRequest,
    Token,
    TokenData,
    GoogleAuthRequest
)

__all__ = [
    # User schemas
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserInBlog",
    
    # Blog schemas
    "BlogBase",
    "BlogCreate",
    "BlogUpdate",
    "BlogResponse",
    "CommentInBlog",
    
    # Comment schemas
    "CommentBase",
    "CommentCreate",
    "CommentUpdate",
    "CommentResponse",
    
    # Auth schemas
    "LoginRequest",
    "Token",
    "TokenData",
    "GoogleAuthRequest",
]
