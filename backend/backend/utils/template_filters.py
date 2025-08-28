from datetime import datetime
import locale
from typing import Union, Optional
import json

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def date_filter(value: Union[str, datetime], format: str = '%B %d, %Y') -> str:
    """
    Format a date string or datetime object.
    
    Args:
        value: Date string (YYYY-MM-DD) or datetime object
        format: Optional format string (default: Month DD, YYYY)
    
    Returns:
        Formatted date string
    """
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            raise ValueError(f"Invalid date format. Expected YYYY-MM-DD, got {value}")
    
    return value.strftime(format)

def currency_filter(value: Union[str, float, int], symbol: str = '$', decimals: int = 2) -> str:
    """
    Format a number as currency.
    
    Args:
        value: Number to format
        symbol: Currency symbol (default: $)
        decimals: Number of decimal places (default: 2)
    
    Returns:
        Formatted currency string
    """
    try:
        if isinstance(value, str):
            value = float(value)
        
        # Validate cents
        if decimals == 2 and round(value * 100) / 100 != value:
            raise ValueError(f"Invalid cents in currency amount: {value}")
        
        return locale.currency(value, symbol=symbol, grouping=True)
    except ValueError as e:
        raise ValueError(f"Invalid currency amount: {value}") from e

def replace_underscore_filter(value: str, capitalize: bool = True) -> str:
    """
    Replace underscores with spaces and optionally capitalize words.
    
    Args:
        value: String with underscores
        capitalize: Whether to capitalize words (default: True)
    
    Returns:
        Formatted string
    """
    if not isinstance(value, str):
        return value
    
    result = value.replace('_', ' ')
    return result.title() if capitalize else result

def phone_filter(value: Optional[str]) -> str:
    """
    Format a phone number consistently.
    
    Args:
        value: Phone number string
    
    Returns:
        Formatted phone number
    """
    if not value:
        return ""
    
    # Remove all non-numeric characters
    numbers = ''.join(filter(str.isdigit, value))
    
    if len(numbers) == 10:
        return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
    elif len(numbers) == 11 and numbers[0] == '1':
        return f"({numbers[1:4]}) {numbers[4:7]}-{numbers[7:]}"
    else:
        return value  # Return original if format unknown

def format_datetime(value, format='%Y-%m-%d %H:%M:%S'):
    """Format a datetime object."""
    if value is None:
        return ''
    if isinstance(value, str):
        try:
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return value
    return value.strftime(format)

def format_currency(value):
    """Format a number as currency."""
    try:
        return f"${float(value):,.2f}"
    except (ValueError, TypeError):
        return value

def to_json(value):
    """Convert a value to JSON string."""
    return json.dumps(value)

def register_filters(app):
    """
    Register all custom filters with the Flask app.
    
    Args:
        app: Flask application instance
    """
    app.jinja_env.filters['date'] = date_filter
    app.jinja_env.filters['currency'] = currency_filter
    app.jinja_env.filters['replace_underscore'] = replace_underscore_filter
    app.jinja_env.filters['phone'] = phone_filter
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['json'] = to_json 