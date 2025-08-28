"""
Database helper utilities for common operations
"""
from typing import List, Dict, Any, Optional, Tuple, Callable
import uuid
from datetime import datetime

def find_by_id(collection: List[Dict], id_value: str, id_field: str = '_id') -> Optional[Dict]:
    """
    Find an item in a collection by its ID
    
    Args:
        collection: The list of dictionaries to search
        id_value: The ID value to find
        id_field: The name of the ID field (default: '_id')
        
    Returns:
        The found item or None if not found
    """
    for item in collection:
        if item.get(id_field) == id_value:
            return item
    return None


def find_by_field(collection: List[Dict], field: str, value: Any) -> List[Dict]:
    """
    Find all items in a collection that match a field value
    
    Args:
        collection: The list of dictionaries to search
        field: The field name to match
        value: The value to match
        
    Returns:
        List of matching items
    """
    return [item for item in collection if item.get(field) == value]


def update_by_id(collection: List[Dict], id_value: str, 
                update_data: Dict, id_field: str = '_id') -> Tuple[bool, Optional[Dict]]:
    """
    Update an item in a collection by its ID
    
    Args:
        collection: The list of dictionaries to update
        id_value: The ID value to find
        update_data: The data to update with
        id_field: The name of the ID field (default: '_id')
        
    Returns:
        Tuple of (success, updated_item)
    """
    for i, item in enumerate(collection):
        if item.get(id_field) == id_value:
            # Keep the original ID
            original_id = item[id_field]
            # Update the item
            collection[i].update(update_data)
            # Ensure ID is preserved
            collection[i][id_field] = original_id
            # Add updated timestamp if not present
            if 'updatedAt' not in update_data:
                collection[i]['updatedAt'] = datetime.utcnow().isoformat()
            return True, collection[i]
    return False, None


def delete_by_id(collection: List[Dict], id_value: str, 
                id_field: str = '_id') -> Tuple[bool, Optional[Dict]]:
    """
    Delete an item from a collection by its ID
    
    Args:
        collection: The list of dictionaries to delete from
        id_value: The ID value to find
        id_field: The name of the ID field (default: '_id')
        
    Returns:
        Tuple of (success, deleted_item)
    """
    for i, item in enumerate(collection):
        if item.get(id_field) == id_value:
            deleted_item = collection.pop(i)
            return True, deleted_item
    return False, None


def create_item(collection: List[Dict], item_data: Dict) -> Dict:
    """
    Create a new item in a collection with standard fields
    
    Args:
        collection: The list to add the item to
        item_data: The item data
        
    Returns:
        The created item
    """
    # Add ID if not present
    if '_id' not in item_data:
        item_data['_id'] = str(uuid.uuid4())
        
    # Add timestamps if not present
    now = datetime.utcnow().isoformat()
    if 'createdAt' not in item_data:
        item_data['createdAt'] = now
    if 'updatedAt' not in item_data:
        item_data['updatedAt'] = now
        
    # Add to collection
    collection.append(item_data)
    
    return item_data


def filter_collection(collection: List[Dict], filter_func: Callable[[Dict], bool]) -> List[Dict]:
    """
    Filter a collection using a custom filter function
    
    Args:
        collection: The list to filter
        filter_func: Function that takes an item and returns True if it should be included
        
    Returns:
        Filtered list
    """
    return [item for item in collection if filter_func(item)] 