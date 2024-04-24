
# to create a schema
from pydantic import BaseModel, EmailStr, Field, conint
from datetime import datetime
from typing import Optional


# creating the schema for the data received from the user

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    created_at: datetime
    email: EmailStr


class UserPwdOut(BaseModel):
    email: EmailStr
    password: str
    id: int
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # default value
    # rating: Optional[int] = None


class PostCreate(PostBase):
    pass


class PostUpdate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(Token):
    id: int


class Vote(BaseModel):
    post_id: int
    dir: int
