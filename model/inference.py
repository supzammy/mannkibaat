from transformers import DistilBertForSequenceClassification, DistilBertTokenizer
import torch
import os

MODEL_DIR = os.path.join(os.path.dirname(__file__), "fine_tuned_model")

_tokenizer = None


def load_model():
    """Load the fine-tuned DistilBERT model from the local model directory.
    Make sure you've placed the model files under model/fine_tuned_model/ (e.g., pytorch_model.bin and config.json).
    """
    if not os.path.isdir(MODEL_DIR):
        raise FileNotFoundError(f"Model directory not found: {MODEL_DIR}. Please add your fine-tuned weights there.")
    model = DistilBertForSequenceClassification.from_pretrained(MODEL_DIR)
    model.eval()
    return model


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        # Use the base tokenizer; if you saved a tokenizer with the fine-tuned model, update this to load from MODEL_DIR
        _tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
    return _tokenizer


def predict_risk(model, tokens, device=None):
    """Given a model and preprocessed tokens, return a risk score (probability of the positive/risk class).

    Inputs:
    - model: loaded Hugging Face model
    - tokens: list of token strings
    - device: optional torch device (e.g., 'cpu' or 'cuda')

    Output:
    - risk_score: float in [0, 1]
    """
    tokenizer = _get_tokenizer()
    text = " ".join(tokens)
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    if device:
        model = model.to(device)
        inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
    probabilities = torch.softmax(outputs.logits, dim=1)
    # Assuming binary classification: index 1 is the 'at risk' class
    risk_score = probabilities[0][1].item()
    return risk_score


def fallback_predict(tokens):
    """A conservative heuristic fallback used when the fine-tuned model isn't available.

    This looks for high-risk phrases and returns a conservative probability in [0,1].
    """
    text = " ".join(tokens).lower()
    # high-signal phrases -> high score
    high_phrases = ["i want to die", "i want to kill myself", "i don't want to live", "suicide", "kill myself"]
    medium_phrases = ["hopeless", "worthless", "no reason to live", "alone", "panic attack"]
    for p in high_phrases:
        if p in text:
            return 0.95
    for p in medium_phrases:
        if p in text:
            return 0.75

    # basic sentiment-ish fallback: presence of words like 'depressed' or 'anxious'
    if "depress" in text or "depressed" in text:
        return 0.7
    if "anxious" in text or "anxiety" in text:
        return 0.55

    # otherwise, return a low-to-medium baseline depending on length
    if len(tokens) < 4:
        return 0.15
    return 0.25
