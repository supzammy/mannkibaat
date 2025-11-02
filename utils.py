"""
Utility functions for risk assessment and helpline information.
"""

from config import RISK_THRESHOLDS, HELPLINE_INFO


def map_score_to_risk(score):
    """
    Map a continuous risk score to a categorical risk level.

    Args:
        score (float): Risk score between 0 and 1.

    Returns:
        str: Risk level ('Low', 'Medium', or 'High').
    """
    if score < RISK_THRESHOLDS["Low"]:
        return "Low"
    elif score < RISK_THRESHOLDS["Medium"]:
        return "Medium"
    else:
        return "High"


def get_helpline_info(risk_level):
    """
    Get helpline and resource information for a given risk level.

    Args:
        risk_level (str): Risk level ('Low', 'Medium', 'High').

    Returns:
        str: Helpline information and recommended actions.
    """
    return HELPLINE_INFO.get(risk_level, HELPLINE_INFO["Default"])


def format_result_message(risk_level, score, used_fallback=False):
    """
    Format a complete result message for display.

    Args:
        risk_level (str): Assessed risk level.
        score (float): Risk score between 0 and 1.
        used_fallback (bool): Whether fallback heuristic was used.

    Returns:
        dict: Formatted result with 'level', 'score', 'helpline', 'warning'.
    """
    result = {
        "level": risk_level,
        "score": score,
        "helpline": get_helpline_info(risk_level),
        "warning": None,
        "used_fallback": used_fallback,
    }

    if risk_level == "High":
        result["warning"] = (
            "⚠️ If you're feeling like you might harm yourself or someone else, "
            "contact local emergency services immediately."
        )

    return result
