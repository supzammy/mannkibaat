"""
Unit tests for utils.py.
"""

import pytest
from utils import map_score_to_risk, get_helpline_info, format_result_message


def test_map_score_to_risk():
    """Test mapping of risk scores to risk levels."""
    assert map_score_to_risk(0.1) == "Low"
    assert map_score_to_risk(0.5) == "Medium"
    assert map_score_to_risk(0.9) == "High"


def test_get_helpline_info():
    """Test retrieval of helpline information."""
    assert "emergency" in get_helpline_info("High").lower()
    assert "counselor" in get_helpline_info("Medium").lower()
    assert "monitor your mood" in get_helpline_info("Low").lower()


def test_format_result_message():
    """Test formatting of result messages."""
    result = format_result_message("High", 0.95, used_fallback=True)
    assert result["level"] == "High"
    assert result["score"] == 0.95
    assert "emergency" in result["warning"].lower()
    assert result["used_fallback"] is True

    result = format_result_message("Low", 0.1, used_fallback=False)
    assert result["level"] == "Low"
    assert result["score"] == 0.1
    assert result["warning"] is None
    assert result["used_fallback"] is False
