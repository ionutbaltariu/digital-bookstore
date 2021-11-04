from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from os import getenv

Base = declarative_base()

DB_TYPE = 'mysql+mysqlconnector'
DB_USER = getenv('DB_USER')
DB_USER_PASS = getenv('DB_USER_PASS')
DB_HOST = 'localhost'
DB_INSTANCE = 'bookstore'
print(DB_USER)
print(DB_USER_PASS)

connection_string = f"{DB_TYPE}://{DB_USER}:{DB_USER_PASS}@{DB_HOST}/{DB_INSTANCE}"

engine = create_engine(connection_string, echo=True, isolation_level="READ UNCOMMITTED")
Session = sessionmaker()