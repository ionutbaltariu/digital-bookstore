from db import Base
from sqlalchemy import Column, String, Integer


class Author(Base):
    __tablename__ = 'authors'
    id = Column(Integer, nullable=False, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Author first_name={self.first_name}, last_name={self.last_name}>"
