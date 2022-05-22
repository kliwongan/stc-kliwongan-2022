from typing import List, Optional
from pydantic import BaseModel

class ItemBase(BaseModel):
    """
    Pydantic model representing a regular item
    to be used in the request body
    """
    title: str
    description: Optional[str] = None
    quantity: int = 0

class ItemCreate(ItemBase):
    """
    Pydantic model representing a regular item
    to be used in the request body;

    NOTE: The pass statement can be replaced
    by any additional parameters that could
    possibly modify the creation of an item
    """
    pass

class Item(ItemBase):
    """
    Pydantic model representing a regular item
    to be used as a response model
    """
    id: int

    # Allow Pydantic to be compatible with ORM models
    class Config:
        orm_mode = True

class DeletedItemBase(BaseModel):
    """
    Pydantic model representing a regular item
    to be used in the request body
    """
    title: str
    description: Optional[str] = None
    quantity: int = 0
    comment: str

class DeletedItemCreate(DeletedItemBase):
    """
    Pydantic model representing a deleted item
    to be used in the request body;

    NOTE: The pass statement can be replaced
    by any additional parameters that could
    possibly modify the creation of an item
    """
    pass

class DeletedItem(DeletedItemBase):
    """
    Pydantic model representing a deleted item
    to be used as a response model
    """
    id: int

    # Allow Pydantic to be compatible with ORM models
    class Config:
        orm_mode = True

