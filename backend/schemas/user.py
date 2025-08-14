from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User email")
    username: str = Field(..., description="Username")
    full_name: str = Field(..., description="Full name")
    password: str = Field(..., description="Password")


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="Password")


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, description="Full name")
    email: Optional[EmailStr] = Field(None, description="Email")
    is_active: Optional[bool] = Field(None, description="Active status")
