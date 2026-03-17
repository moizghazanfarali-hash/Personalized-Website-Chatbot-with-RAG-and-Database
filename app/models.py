from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    name:     str
    email:    EmailStr
    password: str

class LoginRequest(BaseModel):
    email:    EmailStr
    password: str

class AuthResponse(BaseModel):
    message: str
    token:   str
    name:    str
    email:   str

class UserResponse(BaseModel):
    name:  str
    email: str
