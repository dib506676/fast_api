# from pydantic import BaseModel, EmailStr

# class UserCreate(BaseModel):
#     name: str
#     email: EmailStr
#     password: str

# class UserRead(BaseModel):
#     id: int
#     name: str
#     email: EmailStr

#     model_config = dict(from_attributes=True)

# class Token(BaseModel):
#     access_token: str
#     token_type: str

# class BlogBase(BaseModel):
#     title: str
#     content: str

# class BlogCreate(BlogBase):
#     pass

# class BlogRead(BlogBase):
#     id: int
#     user_id: int

#     model_config = dict(from_attributes=True)

# class CommentBase(BaseModel):
#     content: str

# class CommentCreate(CommentBase):
#     blog_id: int

# class CommentRead(CommentBase):
#     id: int
#     user_id: int
#     blog_id: int

#     model_config = dict(from_attributes=True)
