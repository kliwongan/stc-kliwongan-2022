from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Constants
SQL_ALCHEMY_DATABASE_URL = "sqlite:///./app.db"

"""
Initialize SQLAlchemy engine

connect_args check same thread?:
    Allows FastAPI to access the SQL Alchemy database
    to access the same object within the database
    using different threads

"""
engine = create_engine(
    SQL_ALCHEMY_DATABASE_URL,
    connect_args = {
        "check_same_thread": False
    }
)

"""
Each instance of the SessionLocal class will be a database session
These instances will be generated as FastAPI dependencies for the endpoints 
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

# Base class for database ORM model inheritance
Base = declarative_base()