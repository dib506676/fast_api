"""
Blog service
Handles blog CRUD operations
"""
from typing import List, Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from blog.models.blog import Blog
from blog.schemas.blog import BlogCreate, BlogUpdate

class BlogService:
    """Service class for blog operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_blog(self, blog_data: BlogCreate, creator_id: int) -> Blog:
        """
        Create a new blog post
        
        Args:
            blog_data: Blog creation data
            creator_id: ID of the user creating the blog
        
        Returns:
            Blog: Created blog object
        """
        new_blog = Blog(
            title=blog_data.title,
            body=blog_data.body,
            published=blog_data.published,
            creator_id=creator_id
        )
        
        self.db.add(new_blog)
        await self.db.commit()
        await self.db.refresh(new_blog)
        
        return new_blog
    
    async def get_all_blogs(self, skip: int = 0, limit: int = 100) -> List[Blog]:
        """
        Get all published blogs with pagination
        
        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
        
        Returns:
            List[Blog]: List of blog objects
        """
        query = select(Blog).where(Blog.published == True).offset(skip).limit(limit)
        result = await self.db.execute(query)
        blogs = result.scalars().all()
        return list(blogs)
    
    async def get_blog_by_id(self, blog_id: int) -> Optional[Blog]:
        """
        Get blog by ID
        
        Args:
            blog_id: Blog ID
        
        Returns:
            Blog: Blog object if found, None otherwise
        """
        query = select(Blog).where(Blog.id == blog_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_blog(
        self,
        blog_id: int,
        blog_update: BlogUpdate,
        user_id: int
    ) -> Blog:
        """
        Update a blog post
        
        Args:
            blog_id: Blog ID
            blog_update: Blog update data
            user_id: ID of the user updating the blog
        
        Returns:
            Blog: Updated blog object
        
        Raises:
            HTTPException: If blog not found or user not authorized
        """
        blog = await self.get_blog_by_id(blog_id)
        
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with id {blog_id} not found"
            )
        
        # Check authorization
        if blog.creator_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to update this blog"
            )
        
        # Update fields
        blog_data = blog_update.model_dump(exclude_unset=True)
        for key, value in blog_data.items():
            setattr(blog, key, value)
        
        self.db.add(blog)
        await self.db.commit()
        await self.db.refresh(blog)
        
        return blog
    
    async def delete_blog(self, blog_id: int, user_id: int) -> None:
        """
        Delete a blog post
        
        Args:
            blog_id: Blog ID
            user_id: ID of the user deleting the blog
        
        Raises:
            HTTPException: If blog not found or user not authorized
        """
        blog = await self.get_blog_by_id(blog_id)
        
        if not blog:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Blog with id {blog_id} not found"
            )
        
        # Check authorization
        if blog.creator_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this blog"
            )
        
        await self.db.delete(blog)
        await self.db.commit()
