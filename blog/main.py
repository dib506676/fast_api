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
from blog.routers import blog as blog_router  # ← Use alias to avoid conflict

@asynccontextmanager
async def lifespan(app: FastAPI):  # ← Changed back to 'app'
    """
    Lifespan event handler
    Creates database tables on startup
    """
    # Startup
    print("Creating database tables...")
    await create_db_and_tables()
    print("Database tables created successfully!")
    
    yield
    
    # Shutdown
    print("Application shutting down...")

# Create FastAPI app (standard name)
app = FastAPI(  # ← Changed back to 'app'
    title=settings.PROJECT_NAME,
    description="A modern blog API with authentication, comments, and Google OAuth support",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React
        "http://localhost:5173",  # Vite
        "http://localhost:5174",  # Vite (alternative)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers (with blog_router alias)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(blog_router.router)  # ← Use the alias
app.include_router(comment.router)

@app.get("/", tags=["Root"])
def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}!",
        "version": settings.VERSION,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "auth": "/auth",
            "users": "/users",
            "blogs": "/blogs",
            "comments": "/comments"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
