"""
Safety and UPL (Unauthorized Practice of Law) guard for SmartProBono
"""
import re

# Patterns that indicate unauthorized legal advice
ADVICE_PATTERNS = [
    r"\b(i advise|i recommend|you should|you must|you need to)\b",
    r"\b(file .* by|plead .*|sign .*|submit form)\b",
    r"\b(this constitutes legal advice|this is legal advice)\b",
    r"\b(you are required to|you must do|you should do)\b",
    r"\b(hire a lawyer|get a lawyer|contact an attorney)\b",
]

# Patterns that indicate uncertainty (good to escalate)
UNCERTAINTY_PATTERNS = [
    r"\b(i am not sure|i don't know|unclear|uncertain)\b",
    r"\b(consult.*attorney|speak.*lawyer|get.*legal.*help)\b",
    r"\b(this.*complex|this.*complicated|this.*difficult)\b",
]

def needs_escalation(text: str) -> bool:
    """
    Check if text contains unauthorized legal advice or needs escalation
    """
    if not text:
        return True
    
    text_lower = text.lower()
    
    # Check for unauthorized legal advice patterns
    for pattern in ADVICE_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    # Check for uncertainty patterns (good to escalate)
    for pattern in UNCERTAINTY_PATTERNS:
        if re.search(pattern, text_lower):
            return True
    
    # Check for specific legal action words
    legal_action_words = [
        'sue', 'lawsuit', 'litigation', 'file', 'plead', 'defend',
        'prosecute', 'charge', 'arrest', 'convict', 'sentence'
    ]
    
    if any(word in text_lower for word in legal_action_words):
        return True
    
    return False

def sanitize_response(text: str) -> str:
    """
    Sanitize response to remove potentially problematic language
    """
    if not text:
        return text
    
    # Replace problematic phrases
    replacements = {
        'i advise': 'i suggest',
        'you should': 'you might consider',
        'you must': 'you may need to',
        'this is legal advice': 'this is general information',
    }
    
    sanitized = text
    for old, new in replacements.items():
        sanitized = sanitized.replace(old, new)
    
    return sanitized

def add_disclaimer(text: str) -> str:
    """
    Add legal disclaimer to response
    """
    disclaimer = "\n\n⚠️ **Important**: This is general legal information, not legal advice. For specific legal matters, please consult with a qualified attorney."
    
    if "disclaimer" not in text.lower() and "not legal advice" not in text.lower():
        return text + disclaimer
    
    return text
