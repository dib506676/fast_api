"""
Authentication service
Handles user authentication, registration, and Google OAuth
"""
import httpx
from typing import Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from blog.models.user import User, AuthProvider
from blog.core.security import verify_password, get_password_hash
from blog.core.config import settings

class AuthService:
    """Service class for authentication operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def authenticate_user(self, email: str, password: str) -> User:
        """Authenticate user with email and password"""
        email = email.lower().strip()
        
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        user = result.scalar_one_or_none()
        
        if user and user.auth_provider == AuthProvider.GOOGLE and not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "This account was registered with Google. Please use Google login.",
                    "existing_provider": "google",
                    "email": user.email
                }
            )
        
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        return user
    
    async def create_user(
        self,
        email: str,
        password: str,
        full_name: str,
        auth_provider: AuthProvider = AuthProvider.EMAIL
    ) -> User:
        """Create a new user - simplified"""
        email = email.lower().strip()
        hashed_password = get_password_hash(password)
        
        user = User(
            email=email,
            full_name=full_name,
            hashed_password=hashed_password,
            auth_provider=auth_provider
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        query = select(User).where(User.id == user_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        email = email.lower().strip()
        query = select(User).where(User.email == email)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID"""
        query = select(User).where(User.google_id == google_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def create_user_from_google_info(self, google_user_info: Dict[str, Any]) -> User:
        """Create user from Google OAuth information"""
        email = google_user_info['email'].lower().strip()
        
        user = User(
            email=email,
            full_name=google_user_info.get('name', ''),
            google_id=google_user_info['sub'],
            google_email=email,
            auth_provider=AuthProvider.GOOGLE,
            is_verified=True,
            hashed_password=None,
        )
        
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        
        return user
    
    async def link_google_to_existing_user(
        self,
        existing_user: User,
        google_user_info: Dict[str, Any]
    ) -> User:
        """Link Google account to existing email/password user"""
        existing_user.google_id = google_user_info['sub']
        existing_user.google_email = google_user_info['email'].lower().strip()
        
        if not existing_user.full_name:
            existing_user.full_name = google_user_info.get('name', '')
        
        await self.db.commit()
        await self.db.refresh(existing_user)
        
        return existing_user
    
    async def verify_google_token(self, id_token: str) -> Optional[Dict[str, Any]]:
        """Verify Google ID token"""
        try:
            async with httpx.AsyncClient() as client:
                token_response = await client.get(
                    f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}"
                )
                token_response.raise_for_status()
                
                token_info = token_response.json()
                
                if token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
                    return None
                
                return token_info
        
        except Exception as e:
            print(f"Google token verification error: {e}")
            return None
