"""
Blog router
Handles blog CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from typing import List

from blog.core.database import get_session
from blog.schemas.blog import BlogCreate, BlogUpdate, BlogResponse
from blog.models.blog import Blog
from blog.models.user import User
from blog.models.comment import Comment
from blog.dependencies.auth import get_current_user

router = APIRouter(prefix="/blogs", tags=["Blogs"])

@router.get("/", response_model=List[BlogResponse])
async def get_all_blogs(
    session: AsyncSession = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """
    Get all published blogs with creator information
    """
    # Eager load the creator and comments relationships
    query = (
        select(Blog)
        .options(
            selectinload(Blog.creator),
            selectinload(Blog.comments).selectinload(Comment.author)
        )
        .where(Blog.published == True)
        .offset(skip)
        .limit(limit)
        .order_by(Blog.created_at.desc())
    )
    
    result = await session.execute(query)
    blogs = result.scalars().all()
    return blogs

@router.get("/{blog_id}", response_model=BlogResponse)
async def get_blog(
    blog_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get a specific blog by ID with creator and comments
    """
    # Eager load creator, comments, and comment authors
    query = (
        select(Blog)
        .options(
            selectinload(Blog.creator),
            selectinload(Blog.comments).selectinload(Comment.author)
        )
        .where(Blog.id == blog_id)
    )
    
    result = await session.execute(query)
    blog = result.scalar_one_or_none()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    
    return blog

@router.post("/", response_model=BlogResponse, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog_data: BlogCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new blog post
    Requires authentication
    """
    blog = Blog(
        title=blog_data.title,
        body=blog_data.body,
        published=blog_data.published,
        creator_id=current_user.id
    )
    
    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    
    # Reload with creator and comments relationships
    query = (
        select(Blog)
        .options(
            selectinload(Blog.creator),
            selectinload(Blog.comments).selectinload(Comment.author)
        )
        .where(Blog.id == blog.id)
    )
    result = await session.execute(query)
    blog = result.scalar_one()
    
    return blog

@router.put("/{blog_id}", response_model=BlogResponse)
async def update_blog(
    blog_id: int,
    blog_data: BlogUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a blog post
    Only the creator can update their blog
    """
    query = (
        select(Blog)
        .options(
            selectinload(Blog.creator),
            selectinload(Blog.comments).selectinload(Comment.author)
        )
        .where(Blog.id == blog_id)
    )
    result = await session.execute(query)
    blog = result.scalar_one_or_none()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    
    if blog.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this blog"
        )
    
    # Update fields
    blog_data_dict = blog_data.model_dump(exclude_unset=True)
    for key, value in blog_data_dict.items():
        setattr(blog, key, value)
    
    session.add(blog)
    await session.commit()
    await session.refresh(blog)
    
    # Reload with all relationships
    query = (
        select(Blog)
        .options(
            selectinload(Blog.creator),
            selectinload(Blog.comments).selectinload(Comment.author)
        )
        .where(Blog.id == blog.id)
    )
    result = await session.execute(query)
    blog = result.scalar_one()
    
    return blog

@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a blog post
    Only the creator can delete their blog
    """
    query = select(Blog).where(Blog.id == blog_id)
    result = await session.execute(query)
    blog = result.scalar_one_or_none()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {blog_id} not found"
        )
    
    if blog.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this blog"
        )
    
    await session.delete(blog)
    await session.commit()
    
    return None
