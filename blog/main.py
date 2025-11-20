"""
Main FastAPI application
Blog API with authentication and comments
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from blog.core.database import create_db_and_tables
from blog.core.config import settings
from blog.routers import auth, user, comment
from blog.routers import blog as blog_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler
    Runs on startup and shutdown
    """
    # Startup: Create database tables
    await create_db_and_tables()
    yield
    # Shutdown: Clean up resources (if needed)

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A modern blog API with authentication, comments, and Google OAuth support",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-frontend-domain.vercel.app",  # Replace with your actual Vercel frontend URL
        "*"  # Remove this in production for better security
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog_router.router)
app.include_router(comment.router)

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint
    Returns API information
    """
    return {
        "message": "Welcome to Blog API!",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "environment": settings.ENVIRONMENT
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    Used for monitoring and deployment verification
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION
    }

# Export app for Vercel
handler = app

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "blog.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True if settings.ENVIRONMENT == "development" else False
    )
