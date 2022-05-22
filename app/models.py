from sqlalchemy import Column, Integer, String
from .database import Base

class Item(Base):
    """
    Class representing a regular, non-deleted Item
    Can support further relational database type relationships
    (i.e. foreign key relationships)
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(Integer, index=True)

class DeletedItem(Base):
    """
    Class representing an item that has been deleted
    Can support further relational database type relationships
    (i.e. foreign key relationships)
    """

    """
    Note: We do not inherit Item
    since that would imply a foreign key relationship
    between Item and DeletedItem in SQL Alchemy
    
    """
    __tablename__ = "deleted_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    quantity = Column(Integer, index=True)

    # Define the deletion comment
    comment = Column(String, index=True)