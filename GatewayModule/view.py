from pydantic import BaseModel, constr
from typing import Optional


class LoginResponse(BaseModel):
    token: str
    errorMessage: Optional[str]


class RegisterResponse(BaseModel):
    status: str
    errorMessage: Optional[str]


class ValidateResponse(BaseModel):
    status: str
    role: Optional[str]


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class ValidateRequest(BaseModel):
    token: str
