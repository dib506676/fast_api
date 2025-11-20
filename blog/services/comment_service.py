"""
Comment service
Handles comment CRUD operations
"""
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from blog.models.comment import Comment
from blog.schemas.comment import CommentCreate, CommentUpdate

class CommentService:
    """Service class for comment operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_comment(
        self,
        comment_data: CommentCreate,
        author_id: int
    ) -> Comment:
        """
        Create a new comment on a blog post
        
        Args:
            comment_data: Comment creation data
            author_id: ID of the user creating the comment
        
        Returns:
            Comment: Created comment object
        """
        new_comment = Comment(
            content=comment_data.content,
            blog_id=comment_data.blog_id,
            author_id=author_id
        )
        
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        
        return new_comment
    
    async def get_comments_by_blog(self, blog_id: int) -> List[Comment]:
        """
        Get all comments for a specific blog
        
        Args:
            blog_id: Blog ID
        
        Returns:
            List[Comment]: List of comment objects
        """
        query = select(Comment).where(Comment.blog_id == blog_id)
        result = await self.db.execute(query)
        comments = result.scalars().all()
        return list(comments)
    
    async def get_comment_by_id(self, comment_id: int) -> Optional[Comment]:
        """
        Get comment by ID
        
        Args:
            comment_id: Comment ID
        
        Returns:
            Comment: Comment object if found, None otherwise
        """
        query = select(Comment).where(Comment.id == comment_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_comment(
        self,
        comment_id: int,
        comment_update: CommentUpdate,
        user_id: int
    ) -> Comment:
        """
        Update a comment
        
        Args:
            comment_id: Comment ID
            comment_update: Comment update data
            user_id: ID of the user updating the comment
        
        Returns:
            Comment: Updated comment object
        
        Raises:
            HTTPException: If comment not found or user not authorized
        """
        comment = await self.get_comment_by_id(comment_id)
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found"
            )
        
        # Check authorization
        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this comment"
            )
        
        # Update content
        comment.content = comment_update.content
        
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        
        return comment
    
    async def delete_comment(self, comment_id: int, user_id: int) -> None:
        """
        Delete a comment
        
        Args:
            comment_id: Comment ID
            user_id: ID of the user deleting the comment
        
        Raises:
            HTTPException: If comment not found or user not authorized
        """
        comment = await self.get_comment_by_id(comment_id)
        
        if not comment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Comment with id {comment_id} not found"
            )
        
        # Check authorization
        if comment.author_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this comment"
            )
        
        await self.db.delete(comment)
        await self.db.commit()
