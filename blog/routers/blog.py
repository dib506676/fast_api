"""
Blog router
Handles blog CRUD operations
"""
from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from blog.core.database import get_session
from blog.schemas.blog import BlogCreate, BlogUpdate, BlogResponse, BlogDetailResponse
from blog.services.blog_service import BlogService
from blog.dependencies.auth import get_current_user
from blog.models.user import User

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog_data: BlogCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new blog post
    
    Requires authentication
    
    - **title**: Blog title
    - **body**: Blog content
    - **published**: Whether blog is published (default: true)
    """
    blog_service = BlogService(session)
    new_blog = await blog_service.create_blog(blog_data, current_user.id)
    return new_blog

@router.get("/", response_model=List[BlogResponse])
async def get_all_blogs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """
    Get all published blogs with pagination
    
    - **skip**: Number of records to skip (default: 0)
    - **limit**: Maximum number of records (default: 100)
    
    Public endpoint - no authentication required
    """
    blog_service = BlogService(session)
    blogs = await blog_service.get_all_blogs(skip, limit)
    return blogs

@router.get("/{blog_id}", response_model=BlogDetailResponse)
async def get_blog_by_id(
    blog_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get single blog by ID with all comments
    
    Public endpoint - no authentication required
    """
    blog_service = BlogService(session)
    blog = await blog_service.get_blog_by_id(blog_id)
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    
    return blog

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog_update: BlogUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a blog post
    
    Requires authentication
    Only the creator can update their blog
    """
    blog_service = BlogService(session)
    updated_blog = await blog_service.update_blog(blog_id, blog_update, current_user.id)
    return updated_blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a blog post
    
    Requires authentication
    Only the creator can delete their blog
    """
    blog_service = BlogService(session)
    await blog_service.delete_blog(blog_id, current_user.id)
    return None
