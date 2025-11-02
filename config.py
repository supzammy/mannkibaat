"""
Configuration settings and constants for the MannKiBaat application.
"""

# --- Model Configuration ---
# Path to the directory containing the fine-tuned model weights and config.
# The application will look for 'pytorch_model.bin' and 'config.json' here.
MODEL_DIR = "model/fine_tuned_model"

# Hugging Face model name for the tokenizer.
# This should match the base model used for fine-tuning.
TOKENIZER_NAME = "distilbert-base-uncased"


# --- Risk Scoring Configuration ---
# PHQ-8 based thresholds for depression severity
# Score ranges: 0-4 minimal, 5-9 mild, 10-14 moderate, 15-19 moderately severe, 20-27 severe
PHQ8_THRESHOLDS = {
    "Minimal": 4,
    "Mild": 9,
    "Moderate": 14,
    "Moderately Severe": 19,
    "Severe": 27,
}

# Model confidence thresholds for risk level mapping
RISK_THRESHOLDS = {
    "Low": 0.3,
    "Medium": 0.7,
}

# Target confidence range for predictions (85-88% as per documentation)
TARGET_CONFIDENCE_RANGE = (0.85, 0.88)


# --- Helpline and Resource Information ---
# Content to display for each assessed risk level.
HELPLINE_INFO = {
    "Low": (
        "No immediate action needed. Monitor your mood regularly. "
        "If you notice your symptoms worsening, consider talking to a friend or a counselor."
    ),
    "Medium": (
        "Consider reaching out to counselors, support groups, or a mental health professional. "
        "You might find short-term strategies (breathing, grounding) helpful while seeking support."
    ),
    "High": (
        "Immediate professional help advised. Contact AASRA (91-22-2754-6669) or your local emergency services. "
        "If you are in immediate danger, call your local emergency number now."
    ),
    "Default": "Please seek help if you feel unwell. There are resources available to support you.",
}


# --- Fallback Heuristic Keywords ---
# Keywords used by the fallback predictor if the fine-tuned model is not available.
# This provides a basic, conservative risk assessment.
# PHQ-8 symptom domains: interest, mood, sleep, energy, appetite, self-worth, concentration, psychomotor
FALLBACK_KEYWORDS = {
    "high_risk": [
        "i want to die",
        "kill myself",
        "suicide",
        "no reason to live",
        "i want to end it all",
        "better off dead",
        "end my life",
    ],
    "medium_risk": [
        "hopeless",
        "worthless",
        "alone",
        "panic attack",
        "depressed",
        "anxious",
    ],
    # PHQ-8 specific symptom keywords
    "phq8_symptoms": [
        "exhausted",
        "tired",
        "no energy",
        "can't focus",
        "concentrate",
        "sad",
        "down",
        "hopeless",
        "sleep",
        "insomnia",
        "sleeping too much",
        "appetite",
        "eating",
        "worthless",
        "guilt",
        "failure",
        "slowed down",
        "restless",
        "fidgety",
        "moving slowly",
        "no interest",
        "pleasure",
        "enjoy",
    ],
}
