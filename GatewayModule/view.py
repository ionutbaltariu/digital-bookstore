from pydantic import BaseModel, constr, EmailStr
from typing import Optional
from datetime import date


class LoginResponse(BaseModel):
    token: str
    errorMessage: Optional[str]


class RegisterResponse(BaseModel):
    status: str
    errorMessage: Optional[str]


class ValidateResponse(BaseModel):
    status: str
    role: Optional[str]
    id: Optional[int]


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    firstname: constr(min_length=1, max_length=64)
    lastname: constr(min_length=1, max_length=64)
    email: EmailStr
    address: constr(min_length=1, max_length=128)
    birthday: date
    username: str
    password: str


class ValidateRequest(BaseModel):
    token: str
