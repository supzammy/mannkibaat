"""
Model loading, preprocessing, and prediction logic for MannKiBaat.
"""

import re
import os
import torch
from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
from config import MODEL_DIR, TOKENIZER_NAME, FALLBACK_KEYWORDS


# Global cache for model and tokenizer
_model_cache = None
_tokenizer_cache = None


def preprocess_text(text):
    """
    Clean and tokenize input text.

    Args:
        text (str): Raw user input text.

    Returns:
        list: List of cleaned tokens.
    """
    # Convert to lowercase
    text = text.lower()
    # Remove special characters, keep only alphanumeric and spaces
    text = re.sub(r"[^a-z0-9\s]", "", text)
    # Split into tokens
    tokens = text.split()
    return tokens


def load_model():
    """
    Load the fine-tuned DistilBERT model from MODEL_DIR.
    Caches the model in memory after first load.

    Returns:
        model: Loaded DistilBERT model in eval mode.

    Raises:
        FileNotFoundError: If model directory or files don't exist.
        Exception: For other model loading errors.
    """
    global _model_cache

    if _model_cache is not None:
        return _model_cache

    if not os.path.isdir(MODEL_DIR):
        raise FileNotFoundError(
            f"Model directory not found: {MODEL_DIR}. "
            "Please add your fine-tuned model weights there."
        )

    try:
        model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
        model.eval()
        _model_cache = model
        return model
    except Exception as e:
        raise Exception(f"Failed to load model from {MODEL_DIR}: {str(e)}")


def get_tokenizer():
    """
    Load and cache the tokenizer.

    Returns:
        tokenizer: DistilBERT tokenizer.
    """
    global _tokenizer_cache

    if _tokenizer_cache is None:
        _tokenizer_cache = DistilBertTokenizer.from_pretrained(TOKENIZER_NAME)

    return _tokenizer_cache


def predict_risk(model, tokens, device=None):
    """
    Predict risk score using the fine-tuned model.

    Args:
        model: Loaded DistilBERT model.
        tokens (list): Preprocessed text tokens.
        device (str, optional): Torch device ('cpu' or 'cuda').

    Returns:
        float: Risk score between 0 and 1.
    """
    tokenizer = get_tokenizer()
    text = " ".join(tokens)

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

    if device:
        model = model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probabilities = torch.softmax(outputs.logits, dim=1)
    # Assuming binary classification: index 1 is 'at risk' class
    risk_score = probabilities[0][1].item()

    return risk_score


def fallback_predict(tokens):
    """
    Conservative heuristic fallback when the fine-tuned model is unavailable.
    Uses keyword matching to estimate risk level.

    Args:
        tokens (list): Preprocessed text tokens.

    Returns:
        float: Estimated risk score between 0 and 1.
    """
    text = " ".join(tokens).lower()

    # Check for high-risk phrases
    for phrase in FALLBACK_KEYWORDS["high_risk"]:
        if phrase in text:
            return 0.95

    # Check for medium-risk phrases
    for phrase in FALLBACK_KEYWORDS["medium_risk"]:
        if phrase in text:
            return 0.75

    # Basic sentiment fallback
    if "depress" in text or "depressed" in text:
        return 0.7
    if "anxious" in text or "anxiety" in text:
        return 0.55

    # Default low-risk baseline
    if len(tokens) < 4:
        return 0.15

    return 0.25


def get_risk_assessment(user_input):
    """
    Main function to assess risk from user input.
    Tries to use fine-tuned model, falls back to heuristic if unavailable.

    Args:
        user_input (str): Raw user input text.

    Returns:
        tuple: (risk_score, used_fallback)
            - risk_score (float): Score between 0 and 1
            - used_fallback (bool): True if fallback was used
    """
    tokens = preprocess_text(user_input)

    try:
        model = load_model()
        score = predict_risk(model, tokens)
        return score, False
    except Exception:
        # Model not available, use fallback
        score = fallback_predict(tokens)
        return score, True
