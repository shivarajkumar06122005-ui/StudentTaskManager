
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# Registration request
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)


# User response
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    is_active: bool


# Login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# JWT token response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
