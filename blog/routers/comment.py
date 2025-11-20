"""
Comment router
Handles comment CRUD operations
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from typing import List

from blog.core.database import get_session
from blog.schemas.comment import CommentCreate, CommentResponse
from blog.models.comment import Comment
from blog.models.blog import Blog
from blog.models.user import User
from blog.dependencies.auth import get_current_user

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
    """
    from sqlalchemy.orm import selectinload
    
    # Check if blog exists
    blog_query = select(Blog).where(Blog.id == comment_data.blog_id)
    blog_result = await session.execute(blog_query)
    blog = blog_result.scalar_one_or_none()
    
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {comment_data.blog_id} not found"
        )
    
    comment = Comment(
        content=comment_data.content,
        blog_id=comment_data.blog_id,
        author_id=current_user.id
    )
    
    session.add(comment)
    await session.commit()
    await session.refresh(comment)
    
    # Reload with author relationship
    query = (
        select(Comment)
        .options(selectinload(Comment.author))
        .where(Comment.id == comment.id)
    )
    result = await session.execute(query)
    comment = result.scalar_one()
    
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Delete a comment
    Only the comment author can delete their comment
    """
    query = select(Comment).where(Comment.id == comment_id)
    result = await session.execute(query)
    comment = result.scalar_one_or_none()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
    
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment"
        )
    
    await session.delete(comment)
    await session.commit()
    
    return None
