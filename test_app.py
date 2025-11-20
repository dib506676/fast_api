"""Test script to verify all imports work"""
import sys
import asyncio

def test_imports():
    print("=" * 50)
    print("Testing imports...")
    print("=" * 50)
    
    try:
        import fastapi
        print("✅ fastapi imported")
    except Exception as e:
        print(f"❌ fastapi: {e}")
        return False
    
    try:
        import sqlmodel
        print("✅ sqlmodel imported")
    except Exception as e:
        print(f"❌ sqlmodel: {e}")
        return False
    
    try:
        import aiosqlite
        print("✅ aiosqlite imported")
    except Exception as e:
        print(f"❌ aiosqlite: {e}")
        return False
    
    try:
        from pydantic_settings import BaseSettings
        print("✅ pydantic_settings imported")
    except Exception as e:
        print(f"❌ pydantic_settings: {e}")
        return False
    
    try:
        from blog.core.config import settings
        print(f"✅ config loaded: {settings.PROJECT_NAME}")
    except Exception as e:
        print(f"❌ config: {e}")
        return False
    
    try:
        from blog.core.database import create_db_and_tables, get_session
        print("✅ database module loaded")
    except Exception as e:
        print(f"❌ database: {e}")
        return False
    
    try:
        from blog.models import User, Blog, Comment
        print("✅ models loaded")
    except Exception as e:
        print(f"❌ models: {e}")
        return False
    
    try:
        from blog.main import app
        print("✅ main app loaded")
        print(f"✅ App title: {app.title}")
    except Exception as e:
        print(f"❌ main app: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
    print("\nNow run: uvicorn blog.main:app --reload")
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
