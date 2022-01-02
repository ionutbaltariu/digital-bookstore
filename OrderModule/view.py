from pydantic import BaseModel, constr
from fastapi_hypermodel import HyperModel, LinkSet
from typing import List, Dict
from datetime import date


class Book(HyperModel):
    isbn: str
    title: str
    publisher: str
    year_of_publishing: int
    genre: str
    price: float
    stock: int
    links: LinkSet

    class Config:
        orm_mode = True


class IsbnStockPair(BaseModel):
    isbn: str
    quantity: int


class OrderInput(BaseModel):
    user: str
    books: List[IsbnStockPair]


class OrderOutput(HyperModel):
    id: str
    order_date: date
    items: List[Book]
    status: str


class Error(BaseModel):
    error_code: int
    error_source: str
    error_reason: str
