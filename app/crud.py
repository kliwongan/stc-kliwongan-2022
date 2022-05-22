from typing import Callable, Any
from sqlalchemy.orm import Session
from . import models, schemas
from .convert_items import convert_deleted_to_item, convert_item_to_deleted, remove_instance_state

def get_item(db: Session, id: int):
    """
    Returns all items with an id of id

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param id: The id of the item to be found
    :type id: int

    :returns: Query object containing the requested objects
    :rtype: sqlalchemy.orm.Query
    """
    return db.query(models.Item).filter_by(id = id)

def get_deleted_item(db: Session, id: int):
    """
    Returns all deleted items with an id of id

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param id: The id of the item to be found
    :type id: int

    :returns: Query object containing the requested objects
    :rtype: sqlalchemy.orm.Query
    """
    return db.query(models.DeletedItem).filter_by(id = id)

def get_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns all deleted items under specific parameters

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param skip: The index of the item to be skipped
    :type skip: int
    :param limit: The maximum number of returned objects
    :type limit: int

    :returns: Query object containing the requested objects
    :rtype: sqlalchemy.orm.Query
    """
    return db.query(models.Item).offset(skip).limit(limit).all()

def get_deleted_items(db: Session, skip: int = 0, limit: int = 100):
    """
    Returns all deleted items under specific parameters

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param skip: The index of the item to be skipped
    :type skip: int
    :param limit: The maximum number of returned objects
    :type limit: int

    :returns: Query object containing the requested objects
    :rtype: sqlalchemy.orm.Query
    """
    return db.query(models.DeletedItem).offset(skip).limit(limit).all()

def create_item_from_dict(db: Session, item: dict) -> models.Item:
    """
    Creates a regular item from a dictionary representation

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item: Dictionary representation of a regular item
    :type item: dict

    :returns: The newly created item
    :rtype: models.Item
    """
    db_item = models.Item(**item)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def create_item(db: Session, item: schemas.ItemCreate) -> models.Item:
    """
    Creates a regular item from the Pydantic model

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item: Pydantic model representing request body for item creation
    :type item: dict

    :returns: The newly created item
    :rtype: models.Item
    """
    return create_item_from_dict(db, item.dict())

def update_item_from_dict(db: Session, item_id: int, update_item: dict) -> models.Item:

    """
    Updates an item based on new key/value pairs specified by a dictionary

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item_id: The id of the item to be deleted
    :type item_id: int
    :param update_item: Dictionary representing key value pairs the item should be updated to
    :type update_item: dict
    
    :return: The newly updated item
    :rtype: models.Item
    """

    # Get the item
    cur_item = get_item(db, item_id)

    cur_item.update(update_item)
    actual_item = cur_item.first()
    
    db.commit()
    db.refresh(actual_item)

    return actual_item

def update_item(db: Session, item_id: int, update: schemas.ItemCreate) -> models.Item:
    """
    Updates an item based on an item creation schema

    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item_id: The id of the item to be deleted
    :type item_id: int
    :param update: Item creation schema representing item values to be updated to
    :type update: schemas.ItemCreate
    
    :return: The newly updated item
    :rtype: models.Item
    """
    return update_item_from_dict(db, item_id, update.dict())


def delete_item(db: Session, item_id: int, 
                callback: Callable[[Session, models.Item, str], Any], comment: str = "") -> None:

    """
    Deletes an item from the database
    
    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item_id: The id of the item to be deleted
    :type item_id: int
    :param callback: Callback function that is called during deletion, prior to commit
    :type callback: Callable(Session, models.Item, str) -> Any
    :param comment: The deletion comment
    :type comment: str
    
    :rtype: None
    """

    # Try to find the item, if the item is not found, raise an exception
    cur_item = get_item(db, item_id)
    actual_item  = cur_item.first()

    if not cur_item:
        raise Exception("Item not found")

    # Mark the item for deletion
    cur_item.delete()

    # Run callback function
    callback(db, actual_item, comment)

    # Commit database changes
    db.commit()

# Callback function for appending into "deleted" items table
def create_deleted_item(db: Session, item: models.Item, comment: str = "") -> models.DeletedItem:
    """
    Creates a deleted item from an item object
    Acts as a callback function for when a regular item is deleted
    
    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item: The item object to create a deleted item from
    :type item: models.Item
    :param comment: The deletion comment
    :type comment: str
    
    :returns: The newly created deleted item
    :rtype: models.DeletedItem
    """

    init_dict = convert_item_to_deleted(item, comment)
    db_item = models.DeletedItem(**remove_instance_state(init_dict))
    db.add(db_item)
    db.commit()
    db.refresh(db_item)

    return db_item

def delete_item_with_undelete(db: Session, item_id: int, comment: str = "") -> None:
    """
    Deletes an item from the database,
    and defines the create_deleted_item function as a callback function
    
    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param item_id: The id of the item to be deleted
    :type item_id: int
    :param callback: Callback function that is called during deletion, prior to commit
    :type callback: Callable(Session, models.Item, str) -> Any
    :param comment: The deletion comment
    :type comment: str
    
    :rtype: None
    """
    delete_item(db, item_id, callback = create_deleted_item, comment=comment)

def undelete(db: Session, id: int) -> models.Item:
    """
    Undeletes an item from the database
    Acts as a callback function for when a regular item is deleted
    
    :param db: The current database connection session
    :type db: sqlalchemy.orm.Session (or Session)
    :param id: The id of the deleted item to be restored
    :type id: int
    
    :returns: The newly created regular item (by undeletion)
    :rtype: models.DeletedItem
    """

    # When undeleting, we remove the undeleted item from the "deleted items database"
    # and add it back to the regular "items" database

    # Get the deleted item
    cur_deleted_item = get_deleted_item(db, id)

    # Generate item from deleted item
    new_item = convert_deleted_to_item(cur_deleted_item.first())

    # Mark the deleted item for deletion
    cur_deleted_item.delete()

    # Push changes to database
    db.commit()

    # Add it to the items db as a "new" item with a "new" id
    return create_item_from_dict(db, remove_instance_state(new_item))
