# from sqlmodel import select, Session
# from .models import Blog, User, Comment

# # Blog operations
# def create_blog(session: Session, blog: Blog):
#     session.add(blog)
#     session.commit()
#     session.refresh(blog)
#     return blog

# def get_blogs(session: Session):
#     return session.exec(select(Blog)).all()

# def get_blog(session: Session, blog_id: int):
#     return session.get(Blog, blog_id)

# def update_blog(session: Session, blog_id: int, updated_data: dict):
#     blog = session.get(Blog, blog_id)
#     if not blog:
#         return None
#     for key, value in updated_data.items():
#         setattr(blog, key, value)
#     session.add(blog)
#     session.commit()
#     session.refresh(blog)
#     return blog

# def delete_blog(session: Session, blog_id: int):
#     blog = session.get(Blog, blog_id)
#     if not blog:
#         return False
#     session.delete(blog)
#     session.commit()
#     return True

# # Comment operations
# def create_comment(session: Session, comment: Comment):
#     session.add(comment)
#     session.commit()
#     session.refresh(comment)
#     return comment

# def get_comments_by_blog(session: Session, blog_id: int):
#     statement = select(Comment).where(Comment.blog_id == blog_id)
#     return session.exec(statement).all()

# # User operations
# def get_user(session: Session, user_id: int):
#     return session.get(User, user_id)

# def get_user_by_email(session: Session, email: str):
#     statement = select(User).where(User.email == email)
#     return session.exec(statement).first()

