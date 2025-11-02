"""
Unit tests for model.py.
"""

import pytest
from model import preprocess_text, load_model, get_risk_assessment, fallback_predict


def test_preprocess_text():
    """Test text preprocessing logic."""
    raw_text = "Hello, World! This is a test."
    expected_tokens = ["hello", "world", "this", "is", "a", "test"]
    assert preprocess_text(raw_text) == expected_tokens


def test_fallback_predict():
    """Test fallback heuristic logic."""
    tokens_high_risk = ["I", "want", "to", "end", "it", "all"]
    tokens_medium_risk = ["I", "feel", "anxious"]
    tokens_low_risk = ["I", "am", "okay"]

    assert fallback_predict(tokens_high_risk) == pytest.approx(0.95, 0.01)
    assert fallback_predict(tokens_medium_risk) == pytest.approx(0.75, 0.01)
    assert fallback_predict(tokens_low_risk) == pytest.approx(0.15, 0.01)


def test_get_risk_assessment():
    """Test risk assessment logic with fallback."""
    user_input = "I feel very depressed and anxious."
    score, used_fallback = get_risk_assessment(user_input)

    assert used_fallback is True
    assert score == pytest.approx(0.75, 0.01)


@pytest.mark.skip(reason="Model weights not available for testing.")
def test_load_model():
    """Test model loading logic."""
    model = load_model()
    assert model is not None
