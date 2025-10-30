def map_score_to_risk(score):
    if score < 0.3:
        return "Low"
    elif score < 0.7:
        return "Medium"
    else:
        return "High"


def get_helpline_info(risk):
    # Provide slightly richer guidance strings inspired by the attached PDF
    helplines = {
        "Low": (
            "No immediate action needed. Monitor your mood regularly. "
            "If you notice your symptoms worsening, consider talking to a friend or a counselor."
        ),
        "Medium": (
            "Consider reaching out to counselors, support groups, or a mental health professional. "
            "You might find short-term strategies (breathing, grounding) helpful while seeking support."
        ),
        "High": (
            "Immediate professional help advised. Contact AASRA - 91-22-2754-6669 or your local emergency services. "
            "If you are in immediate danger, call your local emergency number now."
        ),
    }
    return helplines.get(risk, "Please seek help if you feel unwell.")
