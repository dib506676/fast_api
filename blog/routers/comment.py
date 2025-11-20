"""
Comment router
Handles comment CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List

from blog.core.database import get_session
from blog.schemas.comment import CommentCreate, CommentUpdate, CommentResponse
from blog.services.comment_service import CommentService
from blog.dependencies.auth import get_current_user
from blog.models.user import User

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Create a new comment on a blog post
    
    Requires authentication
    
    - **content**: Comment content
    - **blog_id**: ID of the blog to comment on
    """
    comment_service = CommentService(session)
    new_comment = await comment_service.create_comment(comment_data, current_user.id)
    return new_comment

@router.get("/blog/{blog_id}", response_model=List[CommentResponse])
async def get_comments_by_blog(
    blog_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Get all comments for a specific blog
    
    Public endpoint - no authentication required
    """
    comment_service = CommentService(session)
    comments = await comment_service.get_comments_by_blog(blog_id)
    return comments

@router.put("/{comment_id}", response_model=CommentResponse)
async def update_comment(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update a comment
    
    Requires authentication
    Only the author can update their comment
    """
    comment_service = CommentService(session)
    updated_comment = await comment_service.update_comment(
        comment_id, comment_update, current_user.id
    )
    return updated_comment

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a comment
    
    Requires authentication
    Only the author can delete their comment
    """
    comment_service = CommentService(session)
    await comment_service.delete_comment(comment_id, current_user.id)
    return None
