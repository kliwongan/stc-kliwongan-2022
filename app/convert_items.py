from . import models

def remove_instance_state(values: dict) -> dict:

    """
    Removes unneccessary keys such as instance state and id
    since these values are not necessary in conversion
    to a new item.

    :param values: A dictionary representing the values of an object
                    generally either a models.Item or models.DeletedItem instance
    :type values: dict

    :returns: Dictionary with the specified keys removed
    :rtype: dict
    
    """

    # Remove unnecessary instance state and id keys
    # Removing the id is necessary so a new unique id can be assigned
    values.pop("_sa_instance_state")
    values.pop("id")
    return values

def convert_item_to_deleted(item: models.Item, comment: str = "") -> dict:

    """
    Converts a non-deleted item to a deleted item
    by returning the item's dictionary representation of a deleted item
    (to be used as keyword arguments in the ctor)

    :param item: The item to be converted
    :type db: models.Item
    :param comment: The deletion comment to be added
    :type comment: str

    :returns: The dictionary representation of a deleted item
    :rtype: dict
    """

    # Programmatically get the relevant attributes from
    # item and move them into a dictionary
    
    item_dict = vars(item)

    # Initialize deletion comment
    item_dict["comment"] = comment

    return item_dict

# Convert a deleted item to a "regular" item
def convert_deleted_to_item(deleted: models.DeletedItem) -> dict:

    """
    Converts a non-deleted item to a deleted item
    by returning the dictionary representation of a non-deleted item
    in the deleted item format (to be used as keyword arguments in the ctor)

    :param item: The deleted item to be converted
    :type db: models.DeletedItem

    :returns: The dictionary representation of a non-deleted item
    :rtype: dict
    """

    # Programmatically get the relevant attributes from
    # deleted item and move them into a dictionary

    item_dict = vars(deleted)

    # Remove deletion comment
    item_dict.pop("comment")

    return item_dict
