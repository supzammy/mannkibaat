import re

def preprocess_text(text):
    """Basic cleaning: remove special characters, lowercase, and tokenize."""
    text = text.lower()
    # Keep basic punctuation if you prefer; here we strip everything except alphanumerics and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    return tokens
