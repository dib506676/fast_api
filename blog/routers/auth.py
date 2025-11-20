"""
Authentication router
Handles login, signup, and Google OAuth
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession

from blog.core.database import get_session
from blog.core.security import create_access_token
from blog.schemas.auth import Token, GoogleAuthRequest
from blog.schemas.user import UserCreate, UserResponse
from blog.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user with email, full name, and password
    
    - **email**: User email (must be unique)
    - **password**: User password (will be hashed)
    - **full_name**: User's full name
    """
    auth_service = AuthService(session)
    
    # Check if user already exists
    existing_user = await auth_service.get_user_by_email(user_data.email)
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user - SIMPLIFIED (no extra fields)
    new_user = await auth_service.create_user(
        email=user_data.email,
        password=user_data.password,
        full_name=user_data.full_name
    )
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """
    Login with email and password
    
    - **username**: User email
    - **password**: User password
    
    Returns JWT access token for authenticated requests
    """
    auth_service = AuthService(session)
    
    # Authenticate user
    user = await auth_service.authenticate_user(form_data.username, form_data.password)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }

@router.post("/google", response_model=Token)
async def google_auth(
    request: GoogleAuthRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate with Google ID token
    
    - **id_token**: Google ID token from frontend
    
    Creates new user if doesn't exist, or links Google account to existing user
    """
    auth_service = AuthService(session)
    
    # Verify Google token
    google_user_info = await auth_service.verify_google_token(request.id_token)
    
    if not google_user_info:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google token"
        )
    
    # Check if user exists by Google ID
    user = await auth_service.get_user_by_google_id(google_user_info['sub'])
    
    if not user:
        # Check if user exists by email
        user = await auth_service.get_user_by_email(google_user_info['email'])
        
        if user:
            # Link Google account to existing email user
            user = await auth_service.link_google_to_existing_user(user, google_user_info)
        else:
            # Create new user from Google info
            user = await auth_service.create_user_from_google_info(google_user_info)
    
    # Create access token
    access_token = create_access_token(data={"sub": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }
