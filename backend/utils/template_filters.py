"""
Template filters for Jinja2 templates.
"""
from datetime import datetime
import json
import locale

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    # Fallback if the locale is not available
    pass

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

def replace_underscore(value, capitalize=True):
    """Replace underscores with spaces and optionally capitalize words."""
    if not isinstance(value, str):
        return value
    
    result = value.replace('_', ' ')
    return result.title() if capitalize else result

def phone_format(value):
    """Format a phone number consistently."""
    if not value:
        return ""
    
    # Remove all non-numeric characters
    numbers = ''.join(filter(str.isdigit, value))
    
    if len(numbers) == 10:
        return f"({numbers[:3]}) {numbers[3:6]}-{numbers[6:]}"
    elif len(numbers) == 11 and numbers[0] == '1':
        return f"({numbers[1:4]}) {numbers[4:7]}-{numbers[7:]}"
    else:
        return value

def register_filters(app):
    """Register custom template filters with the Flask app."""
    app.jinja_env.filters['datetime'] = format_datetime
    app.jinja_env.filters['currency'] = format_currency
    app.jinja_env.filters['json'] = to_json
    app.jinja_env.filters['replace_underscore'] = replace_underscore
    app.jinja_env.filters['phone'] = phone_format 